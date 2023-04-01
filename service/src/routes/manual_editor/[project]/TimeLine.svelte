<script lang="ts">
  import {onMount} from "svelte";
  import {currentTime} from './stores'

  import WaveForm from "./WaveForm.svelte";

  let lastMouseDown
  let timestamps = []

  export let paused
  export let description
  export let duration
  export let audioSrc = ''

  let audioCtx, source, audioData;
  onMount(async () => {
    audioCtx = new AudioContext();

    audioData = await fetch(audioSrc)
      .then(r => r.arrayBuffer())
      .then(arrayBuffer => audioCtx.decodeAudioData(arrayBuffer))
      .then(audioBuffer => audioBuffer.getChannelData(0))
  })

  function minutesToTime(mins) {
      let date = new Date(0)
      date.setMinutes(mins)
      return date.toISOString().substring(11, 19);
  }

  function handleMousedown(e) {
    lastMouseDown = new Date();
  }

  function handleMouseup(e) {
    if (new Date() - lastMouseDown < 300) {
      if (paused) e.target.play();
      else e.target.pause();
    }
  }

  function handleMove(e) {
    if (!duration) return; // video not loaded yet
    if (e.type !== 'touchmove' && !(e.buttons & 1)) return;

    const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
    const {left, right} = this.offsetParent.getBoundingClientRect();
    $currentTime = duration * (clientX - left) / (right - left);
  }

  $: {
      timestamps = []
      let width = containerWidth / duration * 60
      for (let timestamp_ind = 0; timestamp_ind < Math.ceil(duration / 60); timestamp_ind++) {
        if ((timestamp_ind + 1) * 60 > duration) {
            timestamps = [...timestamps, (duration - timestamp_ind * 60) / 60 * width]
        } else {
            timestamps = [...timestamps, width]
        }

      }
  }
  let audioElement
  let containerWidth
</script>

<audio bind:this={audioElement} hidden src={audioSrc}></audio>
<div bind:clientWidth={containerWidth} class="mb-3" style="min-height: 200px">
  <div id="timestamps-wrapper">
    {#each timestamps as timestamp, time}
    <div class="timestamp" style="width: {timestamp}px">
      <p class="text-gray-500 ml-2">{minutesToTime(time)}</p>
    </div>
  {/each}
  </div>
  <div id="tracker-wrapper"
       on:mousemove={handleMove}
       on:touchmove|preventDefault={handleMove}
       on:mousedown={handleMousedown}
       on:mouseup={handleMouseup}>
    <div id="tracker" style="left: calc({$currentTime / duration * 100}% - 5px);">
      <svg width="10px" height="100%">
        <polygon points="0, 0 5, 10 10, 0"
          fill="#e36a18" stroke-width="0"
        />
        <line x1="5" y1="0" x2="5" y2="100%" stroke="#e36a18" stroke-width="2"/>
      </svg>
    </div>
  </div>
  {#if description?.timeline }
    <div id="frames-wrapper" class="pt-8">
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
      z-index: 10;
  }

  #frames-wrapper img {
      height: 100%;
      width: calc(100% / 10);
            z-index: 10;
  }

  #timestamps-wrapper {
      position: absolute;
      height: 100%;
      width: 100%;
      display: flex;
      z-index: 9;
  }

  .timestamp {
      width: 100%;
      border-left: 1px solid #585f6c;
      z-index: 9;
  }

  #tracker-wrapper {
      position: absolute;
      height: 100%;
      width: 100%;
      z-index: 1000;
  }

  #tracker {
      height: 100%;
      width: 10px;
      position: absolute;
  }

  #tracker:hover {
      cursor: ew-resize;
  }
</style>
