<script lang="ts">
  import ProjectCard from './components/ProjectCard.svelte'
  import {CUTTER_URL} from "$lib/constants";
  import {onMount} from "svelte";

  let projects: unknown[] = []

  onMount(async () => {
    projects = await fetch(new URL('/get_all_projects', CUTTER_URL)).then(r => r.json())
  })
</script>

<svelte:head>
	<title>Редактор видео</title>
	<meta name="description" content="Video Editor" />
</svelte:head>
<div class="flex flex-col items-center w-full h-screen">
  <h1 class="text-4xl font-black text-gray-500 text-center mt-20">Выбор проекта</h1>

  <div class="bg-gray-900  grid grid-cols-2 gap-5 place-items-center mt-10">
  <!--  <p>{JSON.stringify(projects)}</p>-->
    {#each projects as project}
      <ProjectCard {...project}/>
      <ProjectCard {...project}/>
      <ProjectCard {...project}/>
      <ProjectCard {...project}/>
      <ProjectCard {...project}/>
      <ProjectCard {...project}/>
    {/each}
  </div>
</div>
<style>

</style>
