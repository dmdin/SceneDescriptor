<script lang="ts">
  import {Trash, Microphone, Stop, Bolt, Play, Pause} from 'svelte-heros-v2'
  import Recorder from "./Recorder.svelte";
  import {capture} from "./frame";

  export let description
  export let time

  export let pointData;

  async function generateText() {
    const video = document.getElementById("video-main") as HTMLVideoElement;

    function capture() {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d")
      if (!ctx) return
      ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

      img.src = canvas.toDataURL("image/png");
    }
    capture()

    console.log(canvas.toDataURL('image/png'))
  }

  let canvas, img
</script>


<img bind:this={img}>
<canvas bind:this={canvas} hidden></canvas>

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
      bind:value={description}></textarea>
  </div>

  <div class="mt-2">
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Запись звука:</p>
      <button title="Сгенерировать озвучку" class="transition transition-color hover:text-yellow-400">
        <Bolt size="20"/>
      </button>
    </div>
    <Recorder/>
  </div>



  <hr class="border-gray-800 mt-2">
  <div class="w-full text-gray-500 text-sm flex justify-between items-end flex-1">
    <p class="mr-1">Удалить маркер:</p>
    <button title="Сгенерировать текст" class="transition transition-color hover:text-red-600 ">
      <Trash size="20"/>
    </button>
  </div>
</div>