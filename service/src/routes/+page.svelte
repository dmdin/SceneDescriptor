<script lang="ts">
  import ProjectCard from '$lib/components/ProjectCard.svelte'
  import Uploader from '$lib/components/Uploader.svelte';
  import {CUTTER_URL} from "$lib/constants";
  import {onMount} from "svelte";

  let projects: unknown[] = []
  
  onMount(async () => {
    getProjects();
  })
  
  async function getProjects(){
    projects = await fetch(new URL('/get_all_projects', CUTTER_URL)).then(r => r.json())
    console.log(projects);
  }

</script>

<svelte:head>
	<title>Редактор видео</title>
	<meta name="description" content="Video Editor" />
</svelte:head>

<div class="flex flex-col items-center w-full h-screen">
  <h1 class="text-4xl font-black text-gray-500 text-center mt-20">Выбор проекта</h1>

  <div class="bg-gray-900 w-4/5 grid grid-cols-2 gap-5 place-items-center mt-10 max-w-5xl">
    {#each projects as project}
      <ProjectCard {...project}/>
    {/each}

    <Uploader on:success_creation={getProjects}/>
  </div>

  
</div>

<style>

</style>
