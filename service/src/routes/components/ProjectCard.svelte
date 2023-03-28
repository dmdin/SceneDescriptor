<script lang="ts">
  import {onMount} from "svelte";

  export let description
  export let video
  export let preview
  export let audio

  let name = ''

  onMount(async () => {
    name = await fetch(description).then(r => r.json())
  })

</script>

<div class="max-w-sm bg-gray-900 rounded-lg shadow border border-2 border-transparent transition transition-colors hover:border-orange-600 cursor-pointer">
  <img class="rounded-t-lg" src={preview} alt="Preview"/>
  <div class="p-2">
    <h5 class="mb-1 text-xl font-normal text-center tracking-tight text-gray-300">Матрица</h5>
  </div>
</div>

<style>
</style>