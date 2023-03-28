<script lang="ts">
  import {drawPCM, getPCM} from './waveform.ts'
  import {onMount} from "svelte";

  export let width = 640
  export let height = 200;
  export let playhead;

  export let audioChunks;
  export let stream;

  let pcm, audioCtx

  onMount(() => {
    audioCtx = new AudioContext()
  })

  audioChunks.subscribe(
    async (v) => {
      const currentBlob = new Blob(v, {
        'type': 'audio/webm; codecs=opus'
      })
      pcm = await getPCM(currentBlob, audioCtx)
      console.log(pcm)
      drawPCM(pcm, canvas, playhead)
    }
  )

  let canvas
</script>


<canvas bind:this={canvas} class="w-full">
</canvas>