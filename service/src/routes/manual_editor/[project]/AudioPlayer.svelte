<script lang="ts">
  import {Play, Pause} from 'svelte-heros-v2'

  export let isPlaying = false
  export let audioSrc
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