<script lang="ts">
  import {createEventDispatcher, onMount} from "svelte";

  import {writable} from "svelte/store";
  import {Trash, Microphone, Stop, Bolt, Play, Pause} from 'svelte-heros-v2'

  import WaveForm from './WaveForm.svelte'

  export let isGeneratedVoice
  export let audioSrc
  const dispatch = createEventDispatcher()
  let isRecording = false;
  let mediaRecorder: any;

  let voice = writable([])
  let blob: any;

  let pcm, audioCtx, analyser, source, dataArray, updateInterval

  function startRecording() {
    isRecording = true;

    audioCtx = new AudioContext();
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 2048;
    const bufferLength = analyser.frequencyBinCount;
    dataArray = new Float32Array(bufferLength);

    navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {
      // Web Audio
      source = audioCtx.createMediaStreamSource(stream);
      source.connect(analyser)

      mediaRecorder = new MediaRecorder(stream);

      $voice = [];
      console.log('Start recording')
      mediaRecorder.start();
      mediaRecorder.addEventListener("dataavailable", function (event: any) {
        $voice = $voice.concat(event.data);
      });

      mediaRecorder.addEventListener("stop", function () {
        blob = new Blob($voice, {
          'type': 'audio/webm; codecs=opus'
        });
        dispatch('recorded', blob)
        console.log("Stop recording");
      });

      updateInterval = setInterval(() => {
        analyser.getFloatTimeDomainData(dataArray)
        dataArray = dataArray
      }, 100)

    }).catch(error => {
      console.log(error)
      // alert("Для записи звука необходимо дать разрешение")
      // location.reload()
    })
  }

  async function stopRecording() {
    mediaRecorder.stop();
    await audioCtx.close()
    clearInterval(updateInterval)
    isRecording = false;
  }

</script>


{#if isRecording}
  <button class="transition transition-color hover:text-red-600 cursor-pointer text-gray-600"
          on:click={stopRecording}>
    <Stop/>
  </button>
{:else}
  <button
    class="transition transition-color hover:text-red-600 cursor-pointer text-gray-600"
    on:click={startRecording}
  >
    <Microphone/>
  </button>
{/if}

{#if audioSrc && !isGeneratedVoice}
  <WaveForm data={dataArray} width={200} height={100}/>
{/if}
