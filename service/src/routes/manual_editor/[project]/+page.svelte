<script lang="ts">
  import {onMount} from "svelte";
  import {writable} from "svelte/store";
  import {page} from '$app/stores';
  import {CUTTER_URL} from "$lib/constants";
  import PointEditor from "./PointEditor.svelte";
  import TimeLine from "./TimeLine.svelte";
  import Gallery from "./Gallery.svelte";
  import {Play, Pause, Microphone, Bookmark, Bolt, CloudArrowUp} from 'svelte-heros-v2'

  import {capture} from './frame'
  import {currentTime} from './stores'

  const wavesurfer: any = writable()
  let WaveSurfer: any;

  let projectId = $page.params.project

  let description: object
  let videoUrl = new URL(`projects/${projectId}/video.mp4`, CUTTER_URL)
  let audioUrl = new URL(`projects/${projectId}/video.wav`, CUTTER_URL)
  let descrUrl = new URL(`projects/${projectId}/description.json`, CUTTER_URL)

  onMount(async () => {
    description = await fetch(descrUrl,
      {
        headers: {"Content-Type": "application/json; charset=utf-8", cache: "no-store"}
      }).then(r => r.json())
    console.log('fetch', description)
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

  // управление видео
  let duration: any;
  let paused = true;
  let lastMouseDown: any;

  function handleMove(e) {
    if (!duration) return; // video not loaded yet
    if (e.type !== 'touchmove' && !(e.buttons & 1)) return; // mouse not down

    const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
    const {left, right} = this.getBoundingClientRect();
    $currentTime = duration * (clientX - left) / (right - left);
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
  function new_point(time: number) {
    let time_sec = time - (time % 1);
    point_voc[time_sec] = {name: "test_name", audio_blob: null};
    point_list.push(time_sec);
    point_list = point_list;
  }

  function deleteMarker(time: any) {
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


  // просмотр с заметками
  let state_show_video = false;

  function start_video() {
    state_show_video = true;
    $currentTime = 0;
    paused = false;
    new_list = {};
  }

  let for_audio_checked;
  $: for_audio_checked = check_audio($currentTime);
  let new_list: any = {};

  // TODO режим прослушки с аудио
  function check_audio(time: any) {
    let time_sec = time - (time % 1);
    if (point_voc[time_sec] !== undefined && !new_list[time_sec]) {
      console.log("Запуск аудиозаписи " + time_sec);
      new_list[time_sec] = true
      if (state_show_video) {
        audio.src = URL.createObjectURL(point_voc[time_sec].audio_blob);
        audio.play();
      }
    }
  }

  async function generatePoints() {
    let newPoints = await fetch(new URL(`/description/${projectId}`, CUTTER_URL)).then(r => r.json())
    newPoints.scenes_info.forEach(point => {
      new_point(point.scene[0])
    })
  }

  async function saveProject() {

  }

  let audio
</script>

<audio hidden bind:this={audio} src='' controls></audio>
<div class="min-h-screen">
  <div class="flex p-5 gap-3 h-fit">
    <div class="flex-initial grow-0 ">
      <Gallery/>
    </div>
    <div class="flex-1 flex flex-col  border border-gray-800 items-center shadow-xl rounded-md p-2 h-full">
      <h1 class="text-gray-400 text-xl font-bold">{description?.name}</h1>
      <div class="w-full">
        <video class="p-2 w-full" id="video-main" crossorigin="anonymous"
               style="object-fit:contain; max-height: 500px;"
               bind:currentTime={$currentTime}
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
                    on:click={() => new_point($currentTime)}>
              <Bookmark variation="" size="20"/>
            </button>
            <button
              title="Сохранить проект"
              class="text-gray-600 transition transition-color hover:text-white"
              on:click={saveProject}
            >
              <CloudArrowUp variation="" size="23"/>
            </button>
            <button
              title="Сгенерировать маркеры"
              class="transition transition-color text-gray-600 hover:text-yellow-400 ml-3"
              on:click={generatePoints}
            >
              <Bolt size="20"/>
            </button>
          </div>
          <p class="text-center my-1 text-gray-400">{format($currentTime)} / {format(duration)}</p>
        </div>
      </div>
    </div>
    <div class="flex-initial">
      <PointEditor on:delete={deleteMarker}/>
    </div>
  </div>


  <div class="flex flex-col shadow-xl mt-2 pb-2 rounded-lg">
    <div class="flex px-4 text-lg flex-wrap">
      <div class="w-full mx-4 my-auto bg-gray-200 rounded-full h-2.5 dark:bg-gray-700 cursor-pointer"
           on:mousemove={handleMove}
           on:touchmove|preventDefault={handleMove}
           on:mousedown={handleMousedown}
           on:mouseup={handleMouseup}>
        <div class="bg-orange-600 h-2.5" style={"width: " + (($currentTime / duration) * 100) + "%;"}></div>
      </div>
    </div>


    <div class="flex px-4 mt-1 mb-4 text-lg bg-blue-100">
      <div class="flex mx-4 w-full relative bg-green-100 ">
        {#each point_list as point}
          <button class="absolute cursor-pointer" on:click={() => $currentTime = point}
                  style={"left: calc(" + ((point / duration) * 100) + "% - 8px);"}>
            <Bookmark size="15" class="text-sky-500"/>
          </button>
        {/each}
      </div>
    </div>
    <div class="mt-3 mx-8">
      <TimeLine description={description} duration={duration} paused={paused} audioSrc={audioUrl}/>
    </div>
  </div>
</div>