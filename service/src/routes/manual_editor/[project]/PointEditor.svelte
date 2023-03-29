<script lang="ts">
  import {onMount} from "svelte";
  import {Trash, Microphone, Stop, Bolt, Play, Pause} from 'svelte-heros-v2'
  import Recorder from "./Recorder.svelte";
  import GeneratedVoice from "./GeneratedVoice.svelte";
  import {capture} from "./frame";
  import {DUBBING_URL, CUTTER_URL} from "$lib/constants";
  import {createEventDispatcher} from "svelte";
  import AudioPlayer from "./AudioPlayer.svelte";

  import {Circle} from "svelte-loading-spinners";

  export let time
  export let pointData = {}

  let isGeneratedVoice = false;
  let isGeneratingText = false, isGeneratingVoice = false

  const dispatch = createEventDispatcher()

  async function generateText() {
    if (isGeneratingText) return
    isGeneratingText = true
    const url = capture()
    const file = await fetch(url)
      .then(res => res.blob())
      .then(blob => new File([blob], `${Date.now()}.png`, {type: "image/png"}))
    let data = new FormData()
    data.append('file', file)

    const imgUrl = await fetch(
      new URL('/upload_image', DUBBING_URL),
      {
        method: 'POST',
        body: data
      }
    ).then(r => r.json()).then(r => r.url)

    pointData[time].text = await fetch(
      new URL('/image2text', DUBBING_URL),
      {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: imgUrl}),
      }
    ).then(r => r.json()).then(r => r.text)
    isGeneratingText = false
  }

  async function generateVoice() {
    if (!pointData[time].text) return
    if (isGeneratingVoice) return

    isGeneratingVoice = true
    pointData[time].audio_blob = await fetch(
      new URL('/text2speech', DUBBING_URL),
      {
        method: 'POST',
        headers: {"Content-Type": "application/json; charset=utf-8"},
        body: JSON.stringify({text: pointData[time].text})
      }
    ).then(r => r.json()).then(r => r.url)
    isGeneratingVoice = false
    isGeneratedVoice = true
  }

  async function uploadVoice(blob) {
    const file = blob
    const data = new FormData()
    data.append('file', file)
    isGeneratedVoice = false

    pointData[time].audio_blob = await fetch(
      new URL('/upload_voice', DUBBING_URL),
      {
        method: 'POST',
        body: data
      }
    ).then(r => r.json()).then(r => r.url)


    console.log(isGeneratedVoice)
    console.log(pointData[time].audio_blob)
  }

  function clearAudio() {
    pointData[time].audio_blob = ''
  }
  function deleteMarker() {
    dispatch("delete")
  }

  function secToTime(secs) {
      let date = new Date(0)
      date.setSeconds(secs)
      return date.toISOString().substring(14, 19);
  }

  let canvas, img, fileInput
</script>

<input hidden bind:this={fileInput} type="file">
<canvas bind:this={canvas} hidden id="capture-canvas"></canvas>
<img bind:this={img} crossorigin="anonymous"/>

<div class="border border-gray-800 p-3 rounded-lg flex flex-col h-full max-w-[260px]">
  <p class="text-md text-gray-400 font-bold">Редактирование маркера</p>
  <div class="flex flex-col">
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Время маркера:</p>
      <p>{secToTime(time)}</p>
    </div>
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Текст маркера:</p>
      <button
        title="Сгенерировать текст" class="transition transition-color hover:text-yellow-400 flex gap-2"
        on:click={generateText}
      >
        {#if isGeneratingText}
          <Circle size="20" color="#FF3E00" unit="px" duration="1s"/>
        {/if}
        <Bolt size="20"/>
      </button>
    </div>
    <textarea
      class="
        text-gray-500 py-0.5 px-1 shadow-none rounded-lg bg-transparent
        resize-none border border-gray-800
        ring-transparent
        ring-0 !outline-none
      "
      bind:value={pointData[time].text}></textarea>
  </div>

  <div class="mt-2">
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Запись звука:</p>
      <button
        title="Сгенерировать озвучку" class="transition transition-color hover:text-yellow-400 flex gap-1"
        on:click={generateVoice}
      >
        {#if isGeneratingVoice}
          <Circle size="20" color="#FF3E00" unit="px" duration="1s"/>
        {/if}
        <Bolt size="20"/>
      </button>
    </div>
    <AudioPlayer audioSrc={pointData[time].audio_blob}/>
    {#if isGeneratedVoice && pointData[time].audio_blob}
      <GeneratedVoice audioSrc={pointData[time].audio_blob} {isGeneratedVoice}/>
    {:else}
      <Recorder audioSrc={pointData[time].audio_blob} {isGeneratedVoice} on:recorded={(e) => uploadVoice(e.detail)}/>
    {/if}
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Удалить озвучку:</p>
      <button
        title="Удалить озвучку" class="transition transition-color hover:text-red-600"
        on:click={clearAudio}
      >
        <Trash size="20"/>
      </button>
    </div>
  </div>


  <hr class="border-gray-800 mt-2">
  <div class="w-full text-gray-500 text-sm flex justify-between items-end flex-1">
    <p class="mr-1">Удалить маркер:</p>
    <button
       class="transition transition-color hover:text-red-600 "
      on:click={deleteMarker}
    >
      <Trash size="20"/>
    </button>
  </div>
</div>