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

<div class="bg-gray-800 w-full h-screen grid place-items-center">
  <p>{JSON.stringify(projects)}</p>
  {#each projects as project}
    <ProjectCard {...project}/>
  {/each}
</div>

<style>

</style>
