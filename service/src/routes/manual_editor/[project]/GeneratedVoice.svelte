<script lang="ts">
  import {onMount} from "svelte";
  import WaveForm from "./WaveForm.svelte";

  export let audioSrc
  export let isGeneratedVoice

  let isPlaying = false
  let audioCtx, source, audioData;
  onMount(async () => {
    audioCtx = new AudioContext();

    audioData = await fetch(audioSrc)
      .then(r => r.arrayBuffer())
      .then(arrayBuffer => audioCtx.decodeAudioData(arrayBuffer))
      .then(audioBuffer => audioBuffer.getChannelData(0))
  })

</script>
{#if audioSrc && isGeneratedVoice}
<WaveForm data={audioData} width={200} height={100}/>
{/if}
