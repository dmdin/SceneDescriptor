<script lang="ts">
  import {onMount} from "svelte";
  import {CUTTER_URL} from "$lib/constants";

  import WaveForm from "./WaveForm.svelte";

  export let projectId
  export let description
  export let videoSrc = ''
  export let audioSrc = ''

  let audioCtx, source, audioData;
  onMount(async () => {
    audioCtx = new AudioContext();

    audioData = await fetch(audioSrc)
      .then(r => r.arrayBuffer())
      .then(arrayBuffer => audioCtx.decodeAudioData(arrayBuffer))
      .then(audioBuffer => audioBuffer.getChannelData(0))
  })

  let audioElement
  let containerWidth
</script>

<audio bind:this={audioElement} hidden src={audioSrc}></audio>
<div bind:clientWidth={containerWidth}>
{#if description && description.timeline }
  <div id="frames-wrapper">
    {#each description.timeline as frame}
    <img src={frame} alt="Превью"/>
  {/each}
  </div>
{/if}

{#if audioData}
  <WaveForm data={audioData} width={containerWidth} height="150"/>
{/if}

</div>
<style>

  #frames-wrapper {
      display: flex;
      /*height: 80px;*/
      max-width: 100%;
  }

  #frames-wrapper img {
      height: 100%;
      width: calc(100% / 10);
  }
</style>
