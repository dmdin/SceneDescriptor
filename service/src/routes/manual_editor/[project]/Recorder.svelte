<script lang="ts">
  import {createEventDispatcher, onMount} from "svelte";

  import {writable} from "svelte/store";
  import {Trash, Microphone, Stop, Bolt, Play, Pause} from 'svelte-heros-v2'

  import WaveForm from './WaveForm.svelte'

  const dispatch = createEventDispatcher()
  let isRecording = false;
  let mediaRecorder: any;


  let voice = writable([])
  let blob: any;


  let pcm, audioCtx, analyser, source, dataArray
  onMount(async () => {
      audioCtx = new AudioContext();
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 2048;
      const bufferLength = analyser.frequencyBinCount;
      dataArray = new Float32Array(bufferLength);
  })

  function loop() {
    analyser.getByteTimeDomainData(dataArray)
    console.log(dataArray)
  }

  function startRecording() {
    isRecording = true;
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
    }).catch(error => {
      console.log('Ошибка!')
      // alert("Для записи звука необходимо дать разрешение")
      // location.reload()
    })
  }

  function stopRecording() {
    mediaRecorder.stop();
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


<button class="transition transition-color hover:text-orange-600 cursor-pointer text-gray-600"
        on:click={() => console.log(2)}>
  <Pause/>
</button>
<button class="transition transition-color hover:text-orange-600 cursor-pointer text-gray-600"
        on:click={() => console.log(2)}>
  <Play/>
</button>


<WaveForm audioChunks={voice}/>
