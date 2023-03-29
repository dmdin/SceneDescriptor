<script lang="ts">
  import {Trash, Microphone, Stop, Bolt, Play, Pause} from 'svelte-heros-v2'
  import Recorder from "./Recorder.svelte";
  import GeneratedVoice from "./GeneratedVoice.svelte";
  import {capture} from "./frame";
  import {DUBBING_URL, CUTTER_URL} from "$lib/constants";

  export let description
  export let time

  export let pointData;

  export let markerText = ''

  async function generateText() {
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

    markerText = await fetch(
      new URL('/image2text', DUBBING_URL),
      {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: imgUrl}),
      }
    ).then(r => r.json()).then(r => r.text)
  }

  async function generateVoice() {
    voiceUrl = await fetch(
      new URL('/text2speech', DUBBING_URL),
      {
        method: 'POST',
        headers: {"Content-Type": "application/json; charset=utf-8"},
        body: JSON.stringify({text: markerText})
      }
    ).then(r => r.json()).then(r => r.url)
  }

  let canvas, img, voiceUrl, fileInput
</script>

<input hidden bind:this={fileInput} type="file">
<canvas bind:this={canvas} hidden id="capture-canvas"></canvas>
<img bind:this={img} crossorigin="anonymous"/>

<div class="border border-gray-800 p-3 rounded-lg flex flex-col h-full max-w-[260px]">
  <p class="text-md text-gray-400 font-bold">Редактирование маркера</p>
  <div class="flex flex-col">
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Время маркера:</p>
      <p>1:18 / 4:50</p>
    </div>
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Текст маркера:</p>
      <button
        title="Сгенерировать текст" class="transition transition-color hover:text-yellow-400"
        on:click={generateText}
      >
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
      bind:value={markerText}></textarea>
  </div>

  <div class="mt-2">
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Запись звука:</p>
      <button
        title="Сгенерировать озвучку" class="transition transition-color hover:text-yellow-400"
        on:click={generateVoice}
      >
        <Bolt size="20"/>
      </button>
    </div>
    {#if voiceUrl}
      <GeneratedVoice audioSrc={voiceUrl}/>
    {:else}
      <Recorder/>
    {/if}
  </div>


  <hr class="border-gray-800 mt-2">
  <div class="w-full text-gray-500 text-sm flex justify-between items-end flex-1">
    <p class="mr-1">Удалить маркер:</p>
    <button title="Сгенерировать текст" class="transition transition-color hover:text-red-600 ">
      <Trash size="20"/>
    </button>
  </div>
</div>