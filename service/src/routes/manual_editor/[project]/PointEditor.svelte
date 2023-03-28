<script lang="ts">
  import {Trash, Microphone, Stop, Bolt} from 'svelte-heros-v2'

  export let description
  export let time

</script>


<div class="border border-gray-800 p-3 rounded-lg flex flex-col  h-full">
  <p class="text-md text-gray-400 font-bold">Редактирование маркера</p>
  <div class="flex flex-col">
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Время отметки:</p>
      <p>1:18 / 4:50</p>
    </div>
    <div class="w-full text-gray-500 text-sm flex justify-between items-center mt-2">
      <p class="mr-1 my-2">Текст отметки:</p>
      <button title="Сгенерировать текст" class="transition transition-color hover:text-yellow-400">
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
    <button class="transition transition-color hover:text-red-600 cursor-pointer text-gray-600">
      <Microphone/>
    </button>
    <button class="transition transition-color hover:text-red-600 cursor-pointer text-gray-600"
            on:click={() => console.log(2)}>
      <Stop/>
    </button>
  </div>
  <hr class="border-gray-800 mt-2">
  <div class="w-full text-gray-500 text-sm flex justify-between items-center">
    <p class="mr-1 my-2">Удалить отметку:</p>
    <button title="Сгенерировать текст" class="transition transition-color hover:text-red-600 ">
      <Trash size="20"/>
    </button>
  </div>
</div>