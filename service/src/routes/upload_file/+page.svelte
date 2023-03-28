<script lang="ts">
  import {onMount} from "svelte";
  import {writable} from "svelte/store";

  const wavesurfer: any = writable()
  let WaveSurfer: any;

  onMount(async () => {
    WaveSurfer = (await import('wavesurfer.js')).default;
  })
  // let point_list: any[] = ["25", "6" ];
  // let point_voc: any = {"25": {name: "Test", audio_blob: null}, "6": {name: "Test", audio_blob: null} };

  let point_list: any[] = [];
  let point_voc: any = {};

  // set video
  let set_file: any = null;

  let for_audio: any;
  $:for_audio = file_check(set_file);

  function file_check(file: any) {
    if (set_file !== null) {
      setTimeout(create_audio, 1000);
    }
  }

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
    // $wavesurfer.load('https://sveltejs.github.io/assets/caminandes-llamigos.mp4');
    $wavesurfer.load(window.URL.createObjectURL(set_file[0]));

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
  <div class="h-48 w-80 flex flex-col shadow-xl rounded-xl m-auto mt-40 border border-2 border-orange-600">
    <input accept=".mov, .mp4" hidden id="files" type="file" bind:files={set_file}>
    <p class="text-center text-gray-400 mt-8">Выберете файл для дальнейшего редактирования</p>
    <label for="files">
      <svg width="18" height="18" class="w-14 h-14 mx-auto my-6 cursor-pointer" viewBox="0 0 18 18" fill="none"
           xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd" clip-rule="evenodd"
              d="M12 2H6C3.79086 2 2 3.79086 2 6V12C2 14.2091 3.79086 16 6 16H12C14.2091 16 16 14.2091 16 12V6C16 3.79086 14.2091 2 12 2ZM6 0C2.68629 0 0 2.68629 0 6V12C0 15.3137 2.68629 18 6 18H12C15.3137 18 18 15.3137 18 12V6C18 2.68629 15.3137 0 12 0H6Z"
              fill="#747c87"/>
        <path
          d="M8.10039 4.9501C8.10039 5.69568 7.49598 6.3001 6.75039 6.3001C6.00481 6.3001 5.40039 5.69568 5.40039 4.9501C5.40039 4.20451 6.00481 3.6001 6.75039 3.6001C7.49598 3.6001 8.10039 4.20451 8.10039 4.9501Z"
          fill="#747c87"/>
        <path fill-rule="evenodd" clip-rule="evenodd"
              d="M11.8242 7.38837L16.2683 14.0546L17.9324 12.9452L13.0104 5.56209C12.3715 4.60379 10.9357 4.69317 10.4206 5.72332L7.02957 12.5055L5.64629 10.6611C5.0986 9.93085 4.0311 9.85498 3.38563 10.5004L0.193284 13.6928L1.6075 15.107L4.3922 12.3223L5.91498 14.3527C6.58402 15.2447 7.95795 15.1209 8.45662 14.1235L11.8242 7.38837Z"
              fill="#747c87"/>
      </svg>
    </label>
  </div>
</div>