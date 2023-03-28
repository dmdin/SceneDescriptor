<script lang="ts">
  import {onMount} from "svelte";
  import {writable} from "svelte/store";
  import {page} from '$app/stores';
  import {CUTTER_URL} from "$lib/constants";
  import PointEditor from "./PointEditor.svelte";
  import {Play, Pause, Microphone, Bookmark, Bolt} from 'svelte-heros-v2'

  const wavesurfer: any = writable()
  let WaveSurfer: any;

  let projectId = $page.params.project

  let description: unknown
  let videoUrl = new URL(`projects/${projectId}/video.mp4`, CUTTER_URL)
  let audioUrl = new URL(`projects/${projectId}/video.wav`, CUTTER_URL)
  let descrUrl = new URL(`projects/${projectId}/description.json`, CUTTER_URL)

  onMount(async () => {
    WaveSurfer = (await import('wavesurfer.js')).default;
    description = await fetch(descrUrl).then(r => r.json())

  })
  // let point_list: any[] = ["25", "6" ];
  // let point_voc: any = {"25": {name: "Test", audio_blob: null}, "6": {name: "Test", audio_blob: null} };

  let point_list: any[] = [];
  let point_voc: any = {};

  // set video
  let for_audio: any;
  // $:for_audio = file_check(set_file);

  // function file_check(file: any) {
  //   if (set_file !== null) {
  //     setTimeout(create_audio, 1000);
  //   }
  // }

  function create_audio() {
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
    // console.log(WaveSurfer);
    // $wavesurfer.load(window.URL.createObjectURL(set_file[0]));
    $wavesurfer.load('https://sveltejs.github.io/assets/caminandes-llamigos.mp4');
    // $wavesurfer.load(videoUrl);

  }

  // управление видео
  let time_now = 0;
  let duration: any;
  let paused = true;
  let lastMouseDown: any;

  function handleMove(e) {
    if (!duration) return; // video not loaded yet
    if (e.type !== 'touchmove' && !(e.buttons & 1)) return; // mouse not down

    const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
    const {left, right} = this.getBoundingClientRect();
    time_now = duration * (clientX - left) / (right - left);
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

  function format(seconds) {
    if (isNaN(seconds)) return '...';

    const minutes = Math.floor(seconds / 60);
    seconds = Math.floor(seconds % 60);
    if (seconds < 10) seconds = '0' + seconds;

    return `${minutes}:${seconds}`;
  }

  // поинты
  function new_point(time: any) {
    let time_sec = time - (time % 1);
    point_voc[time_sec] = {name: "test_name", audio_blob: null};
    point_list.push(time_sec);
    point_list = point_list;
  }

  function delete_point(time: any) {
    let time_sec = time - (time % 1);
    delete point_voc[time_sec];
    let new_list: any[] = [];
    point_list.forEach(point => {
      if (point !== time_sec) new_list.push(point);
    })
    point_list = new_list;
  }

  // audio
  let recording_state = false;
  let mediaRecorder: any;

  function start_recording(time) {
    recording_state = true;
    navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {

      mediaRecorder = new MediaRecorder(stream);
      let voice: any[] = [];

      mediaRecorder.start();

      mediaRecorder.addEventListener("dataavailable", function (event: any) {
        voice.push(event.data);
      });

      mediaRecorder.addEventListener("stop", function () {

        point_voc[time - (time % 1)].audio_blob = new Blob(voice, {
          'type': 'audio/webm; codecs=opus'
        });
        console.log("Создание новой дорожки");

      });
      point_voc = point_voc;
    })
  }

  function stop_recording() {
    mediaRecorder.stop();
    recording_state = false;
  }

  // просмотр с заметками
  let state_show_video = false;

  function start_video() {
    state_show_video = true;
    time_now = 0;
    paused = false;
    new_list = {};
  }

  let for_audio_checked;
  $: for_audio_checked = check_audio(time_now);
  let new_list: any = {};

  function check_audio(time: any) {
    let time_sec = time - (time % 1);
    if (point_voc[time_sec] !== undefined && !new_list[time_sec]) {
      console.log("Запуск аудиозаписи " + time_sec);
      new_list[time_sec] = true
      if (state_show_video) {
        document.getElementById("hid_audio").src = URL.createObjectURL(point_voc[time_sec].audio_blob);
        document.getElementById("hid_audio").play();

      }
    }
  }
</script>


<audio hidden id="hid_audio" src='' controls></audio>
<div class="h-screen">
  <div class="flex p-5 gap-3 h-fit">
    <div class="flex flex-col flex-1 border border-gray-800 items-center shadow-xl rounded-md p-2 h-full">
      <div>
      <video class="p-2"
             style="object-fit:contain; max-height: 20rem;"
             bind:currentTime={time_now}
             bind:duration
             bind:paused
      >
        <source src={videoUrl}>
        <track kind="captions">
      </video>
        <div class="flex justify-between w-full px-4">
          <div class="flex gap-2">
            <button class="text-gray-600 transition transition-color hover:text-orange-600"
                    class:text-orange-500={paused}
                    on:click={() => {paused=true}}>
              <Pause variation="solid"/>
            </button>
            <button class="text-gray-600 transition transition-color hover:text-orange-600"
                    class:text-orange-500={!paused}
                    on:click={() => {paused=false}}>
              <Play/>
            </button>
            <button class="text-gray-600 transition transition-color hover:text-sky-500"
                    on:click={() => new_point(time_now)}>
              <Bookmark variation="" size="20"/>
            </button>
            <button
              title="Сгенерировать маркеры"
              class="transition transition-color text-gray-600 hover:text-yellow-400 ml-3"
            >
              <Bolt size="20"/>
            </button>
          </div>
          <p class="text-center my-1 text-gray-400">{format(time_now)} / {format(duration)}</p>
        </div>
      </div>
    </div>
<!--      <div class="flex">-->
        <!-- <button on:click={create_audio} class="btn-blue mx-1 my-1">сгенерить аудио</button> -->
<!--      </div>-->

<!--      <button class="btn-blue mt-1" on:click={start_video}>Запустить видео с заметками</button>-->
    <div class="flex-initial">
      <PointEditor />
    </div>
      <!--{#if point_voc[time_now - (time_now % 1)]}-->
      <!--  <div class="border mt-2 p-1 rounded-lg flex flex-col">-->
      <!--    <p class="text-xs text-gray-400 text-center">Редактирование маркера</p>-->
      <!--    <div class="flex">-->
      <!--      <p class="mr-1 text-gray-600 text-sm my-auto">Текст отметки:</p>-->
      <!--      <input class="p-0.5 rounded-lg" type="text" bind:value={point_voc[time_now - (time_now % 1)].name}>-->
      <!--    </div>-->
      <!--    <p on:click={() => delete_point(time_now)} class="text-xs text-red-500 hover:text-red-400 cursor-pointer">-->
      <!--      Удалить отметку</p>-->


      <!--    {#if point_voc[time_now - (time_now % 1)].audio_blob !== null}-->

      <!--      <div class="flex h-20">-->
      <!--        <audio class="my-auto" src={URL.createObjectURL(point_voc[time_now - (time_now % 1)].audio_blob)}-->
      <!--               controls></audio>-->
      <!--        <button class="bg-red-400 hover:bg-red-300 w-8 h-8 my-auto ml-2 rounded-xl"-->
      <!--                on:click={() => {point_voc[time_now - (time_now % 1)].audio_blob = null}}>-->
      <!--          <svg width="16" height="16" class="m-auto" viewBox="0 0 16 16" fill="none"-->
      <!--               xmlns="http://www.w3.org/2000/svg">-->
      <!--            <path-->
      <!--              d="M0.472396 0.472518C0.758152 0.186848 1.14567 0.0263672 1.54973 0.0263672C1.95379 0.0263672 2.34131 0.186848 2.62706 0.472518L8.01525 5.86071L13.4034 0.472518C13.6908 0.194944 14.0758 0.0413523 14.4753 0.0448241C14.8748 0.048296 15.257 0.208553 15.5395 0.49108C15.8221 0.773607 15.9823 1.1558 15.9858 1.55534C15.9893 1.95487 15.8357 2.33979 15.5581 2.62718L10.1699 8.01537L15.5581 13.4036C15.8357 13.691 15.9893 14.0759 15.9858 14.4754C15.9823 14.875 15.8221 15.2571 15.5395 15.5397C15.257 15.8222 14.8748 15.9825 14.4753 15.9859C14.0758 15.9894 13.6908 15.8358 13.4034 15.5582L8.01525 10.17L2.62706 15.5582C2.33967 15.8358 1.95475 15.9894 1.55521 15.9859C1.15568 15.9825 0.773485 15.8222 0.490958 15.5397C0.208431 15.2571 0.048174 14.875 0.0447021 14.4754C0.0412302 14.0759 0.194822 13.691 0.472396 13.4036L5.86059 8.01537L0.472396 2.62718C0.186726 2.34143 0.0262451 1.95391 0.0262451 1.54985C0.0262451 1.14579 0.186726 0.758274 0.472396 0.472518Z"-->
      <!--              fill="#ffffff"/>-->
      <!--          </svg>-->
      <!--        </button>-->
      <!--      </div>-->
      <!--    {:else}-->
      <!--      {#if !recording_state}-->
      <!--        <button class="btn-blue mt-2 mx-auto" on:click={() => start_recording(time_now)}>-->
      <!--          <Microphone/>-->
      <!--        </button>-->
      <!--      {:else}-->
      <!--        <button class="btn-blue mt-2 mx-auto" on:click={stop_recording}>Остановить запись</button>-->
      <!--      {/if}-->
      <!--    {/if}-->
      <!--  </div>-->
      <!--{:else}-->
      <!--  <button on:click={() => new_point(time_now)} class="btn-blue mt-2 mx-auto">Создать отметку(?)</button>-->
      <!--{/if}-->
  </div>


  <div class="flex flex-col shadow-xl mt-2 pb-2 rounded-lg">
    <div class="flex px-4 text-lg">
      <div class="w-full mx-4 my-auto bg-gray-200 rounded-full h-2.5 dark:bg-gray-700 cursor-pointer"
           on:mousemove={handleMove}
           on:touchmove|preventDefault={handleMove}
           on:mousedown={handleMousedown}
           on:mouseup={handleMouseup}>
        <div class="bg-orange-600 h-2.5" style={"width: " + ((time_now / duration) * 100) + "%;"}></div>
      </div>
    </div>

    <div class="flex px-4 mt-1 mb-4 text-lg bg-blue-100">
      <div class="flex mx-4 w-full relative bg-green-100 ">
        {#each point_list as point}
          <button class="absolute cursor-pointer" on:click={() => time_now = point}
               style={"left: calc(" + ((point / duration) * 100) + "% - 8px);"}>
            <Bookmark size="15" class="text-sky-500"/>
          </button>
        {/each}
      </div>
    </div>

    <div class="mx-8" id="waveform"></div>

    <!-- {#if paused} -->

    <!-- {/if} -->

  </div>
</div>