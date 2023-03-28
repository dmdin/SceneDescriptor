<script lang="ts">
  import {drawPCM, getPCM} from './waveform.ts'
  import {onMount} from "svelte";

  export let width = 640
  export let height = 200;
  export let playhead;

  export let data;

  // let pcm, audioCtx

  $: if (data && canvas) drawPCM(data, canvas, playhead)


  /*
  audioChunks.subscribe(
    async (v) => {
      console.log(v)
      const currentBlob = new Blob(v, {
        'type': 'audio/webm; codecs=opus'
      })
      const fileReader = new FileReader();
      pcm = await getPCM(currentBlob, audioCtx, fileReader)
      drawPCM(pcm, canvas, playhead)
    }
  )
  */

  let canvas
</script>


<canvas bind:this={canvas} class="w-full">
</canvas>