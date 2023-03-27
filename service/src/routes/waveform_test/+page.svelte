<script context="module">
  export const ssr = false;

</script>

<script>
  import {onMount} from "svelte";
  import {writable} from "svelte/store";

  const wavesurfer = writable()
  onMount(async () => {
    const WaveSurfer = (await import('wavesurfer.js')).default
    console.log(WaveSurfer)
    $wavesurfer = WaveSurfer.create({
      container: '#waveform',
      waveColor: 'rgb(38, 126, 97)',
      progressColor: 'rgb(77, 189, 152)',
      interact: false,
      height: 50,
      responsive: true,
      hideScrollbar: true,
      backend: 'MediaElement'
    });
    $wavesurfer.load('http://localhost:8000/voices/1679943360062.mp3');
    //
    // wavesurfer.on('ready', function () {
    //   wavesurfer.play();
    // });
  })
</script>

<div id="waveform"></div>

<button on:click={() => $wavesurfer.play()}>
  Play
</button>