<script lang="ts">
  import {goto} from "$app/navigation";

  export let description
  export let video
  export let preview
  export let audio
  export let name
  export let id

  export let textCls = 'text-xl'

</script>

<!-- <div class="{$$props.class} bg-gray-900 rounded-lg shadow border border-2 border-transparent transition transition-colors hover:border-orange-600 cursor-pointer" on:click={() => goto(`/manual_editor/${id}`)}> -->
<div class="{$$props.class} bg-gray-900 flex w-full flex-col rounded-lg shadow border-2 border-transparent transition-colors hover:border-orange-600 cursor-pointer" on:click={() => goto(`/manual_editor/${id}`)}>
  <img class="rounded-t-lg my-auto" src={preview} alt="Preview"/>
  <div class="p-2 mt-auto">
    <h5 class="mb-1 {textCls} font-normal text-center tracking-tight text-gray-500">{name}</h5>
  </div>
</div>

<style>
</style>