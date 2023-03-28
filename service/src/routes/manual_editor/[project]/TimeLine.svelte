<script lang="ts">
  import {onMount} from "svelte";
  import {CUTTER_URL} from "$lib/constants";

  export let projectId
  export let description
  export let videoSrc = ''
  export let audioSrc = ''

</script>
{#if description && description.timeline }
  <div id="frames-wrapper">
    {#each description.timeline as frame}
    <img src={frame}/>
  {/each}
  </div>

{/if}

<style>
  #frames-wrapper {
      display: flex;
      height: 80px;
      width: 100%;
  }

  #frames-wrapper img {
      height: 100%;
      width: 100%;
  }
</style>
