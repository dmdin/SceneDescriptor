<script lang="ts">
  import {Trash, Microphone, Stop} from 'svelte-heros-v2'

  export let description
</script>


<div class="border mt-2 p-1 rounded-lg flex flex-col">
  <p class="text-xs text-gray-400 text-center">Редактирование маркера</p>
  <div class="flex">
    <p class="mr-1 text-gray-600 text-sm my-auto">Текст отметки:</p>
    <textarea class="p-0.5 rounded-lg"></textarea>
    <input class="p-0.5 rounded-lg" type="text" bind:value={description}>
  </div>
  <button class="text-xs text-red-500 hover:text-red-400 cursor-pointer">
    <Trash/>
  </button>


  <div class="flex h-20">
    <!--              <audio class="my-auto" src={URL.createObjectURL(point_voc[time_now - (time_now % 1)].audio_blob)}-->
    <!--                     controls></audio>-->
    <button class="bg-red-400 hover:bg-red-300 w-8 h-8 my-auto ml-2 rounded-xl"
            on:click={() => console.log(1)}>
      <svg width="16" height="16" class="m-auto" viewBox="0 0 16 16" fill="none"
           xmlns="http://www.w3.org/2000/svg">
        <path
          d="M0.472396 0.472518C0.758152 0.186848 1.14567 0.0263672 1.54973 0.0263672C1.95379 0.0263672 2.34131 0.186848 2.62706 0.472518L8.01525 5.86071L13.4034 0.472518C13.6908 0.194944 14.0758 0.0413523 14.4753 0.0448241C14.8748 0.048296 15.257 0.208553 15.5395 0.49108C15.8221 0.773607 15.9823 1.1558 15.9858 1.55534C15.9893 1.95487 15.8357 2.33979 15.5581 2.62718L10.1699 8.01537L15.5581 13.4036C15.8357 13.691 15.9893 14.0759 15.9858 14.4754C15.9823 14.875 15.8221 15.2571 15.5395 15.5397C15.257 15.8222 14.8748 15.9825 14.4753 15.9859C14.0758 15.9894 13.6908 15.8358 13.4034 15.5582L8.01525 10.17L2.62706 15.5582C2.33967 15.8358 1.95475 15.9894 1.55521 15.9859C1.15568 15.9825 0.773485 15.8222 0.490958 15.5397C0.208431 15.2571 0.048174 14.875 0.0447021 14.4754C0.0412302 14.0759 0.194822 13.691 0.472396 13.4036L5.86059 8.01537L0.472396 2.62718C0.186726 2.34143 0.0262451 1.95391 0.0262451 1.54985C0.0262451 1.14579 0.186726 0.758274 0.472396 0.472518Z"
          fill="#ffffff"/>
      </svg>
    </button>
  </div>

  <button class="btn-blue mt-2 mx-auto">
    <Microphone/>
  </button>
  <button class="btn-blue mt-2 mx-auto" on:click={() => console.log(2)}>
    <Stop/>
  </button>
</div>