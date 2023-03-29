<script lang="ts">
  import {onMount} from "svelte";
  import {Play, Pause} from 'svelte-heros-v2'
  import WaveForm from "./WaveForm.svelte";

  export let audioSrc = 'http://localhost:8000/voices/1680048398029.mp3'

  let isPlaying = false
  let audioCtx, source, audioData;
  onMount(async () => {
    audioCtx = new AudioContext();

    audioData = await fetch(audioSrc)
      .then(r => r.arrayBuffer())
      .then(arrayBuffer => audioCtx.decodeAudioData(arrayBuffer))
      .then(audioBuffer => audioBuffer.getChannelData(0))
  })


  function pause() {
    isPlaying = false
    audio.pause()
  }

  function play() {
    isPlaying = true
    audio.currentTime = 0
    audio.play()
  }

  let audio
</script>

<audio bind:this={audio} hidden src={audioSrc} loop></audio>
{#if isPlaying}
  <button class="transition transition-color hover:text-orange-600 cursor-pointer text-gray-600"
          on:click={pause}>
    <Pause/>
  </button>
{:else}
  <button class="transition transition-color hover:text-orange-600 cursor-pointer text-gray-600"
          on:click={play}>
    <Play/>
  </button>
{/if}

<WaveForm data={audioData} width={200} height={100}/>
