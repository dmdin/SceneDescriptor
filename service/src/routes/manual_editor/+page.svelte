<script lang="ts">
	import { onMount } from "svelte";
	import {writable} from "svelte/store";

	const wavesurfer: any = writable()
	let WaveSurfer: any;

	onMount(async() => {
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

function file_check(file: any){
	if(set_file !== null){
		setTimeout(create_audio, 1000);
	}
}

function create_audio(){
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
		const { left, right } = this.getBoundingClientRect();
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
	function new_poin(time: any){
		point_voc[time - (time % 1)] = {name: "test_name", audio_blob: null};
		point_list.push(time - (time % 1));
		point_list = point_list;
	}

// audio
	let recording_state = false;
	let mediaRecorder: any;
	
	function start_recording(time){
    recording_state = true;
    navigator.mediaDevices.getUserMedia({ audio: true}).then(stream => {

      mediaRecorder = new MediaRecorder(stream);
      let voice: any[] = [];
      
      mediaRecorder.start();

      mediaRecorder.addEventListener("dataavailable",function(event: any) {
        voice.push(event.data);
      });

      mediaRecorder.addEventListener("stop", function() {

        point_voc[time - (time % 1)].audio_blob = new Blob(voice, {
          'type': 'audio/webm; codecs=opus'
        });
        console.log("Создание новой дорожки");
        
      });
			point_voc = point_voc;
    })  
  }
	function stop_recording(){
    mediaRecorder.stop();
    recording_state = false;
  }

</script>

<div class="">
	{#if !set_file}
		<div class="h-48 w-80 flex flex-col shadow-xl rounded-xl m-auto mt-40">
			<input accept=".mov, .mp4" hidden id="files" type="file" bind:files={set_file}>
			<p class="text-center text-gray-600 mt-8">Выберете файл для дальнейшего редактирования</p>
			<label for="files">
				<svg width="18" height="18" class="w-14 h-14 mx-auto my-6 cursor-pointer" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
					<path fill-rule="evenodd" clip-rule="evenodd" d="M12 2H6C3.79086 2 2 3.79086 2 6V12C2 14.2091 3.79086 16 6 16H12C14.2091 16 16 14.2091 16 12V6C16 3.79086 14.2091 2 12 2ZM6 0C2.68629 0 0 2.68629 0 6V12C0 15.3137 2.68629 18 6 18H12C15.3137 18 18 15.3137 18 12V6C18 2.68629 15.3137 0 12 0H6Z" fill="#747c87"/>
					<path d="M8.10039 4.9501C8.10039 5.69568 7.49598 6.3001 6.75039 6.3001C6.00481 6.3001 5.40039 5.69568 5.40039 4.9501C5.40039 4.20451 6.00481 3.6001 6.75039 3.6001C7.49598 3.6001 8.10039 4.20451 8.10039 4.9501Z" fill="#747c87"/>
					<path fill-rule="evenodd" clip-rule="evenodd" d="M11.8242 7.38837L16.2683 14.0546L17.9324 12.9452L13.0104 5.56209C12.3715 4.60379 10.9357 4.69317 10.4206 5.72332L7.02957 12.5055L5.64629 10.6611C5.0986 9.93085 4.0311 9.85498 3.38563 10.5004L0.193284 13.6928L1.6075 15.107L4.3922 12.3223L5.91498 14.3527C6.58402 15.2447 7.95795 15.1209 8.45662 14.1235L11.8242 7.38837Z" fill="#747c87"/>
				</svg>
			</label>
		</div>

	{:else}

		<div class="flex justify-between">
			<video class="p-2 shadow-xl rounded-lg"
				style="object-fit:contain; max-height: 20rem;"
				bind:currentTime={time_now}
				bind:duration
				bind:paused
			>
				<source src={window.URL.createObjectURL(set_file[0])}>
					<!-- <source src={"https://sveltejs.github.io/assets/caminandes-llamigos.mp4"}> -->
				<track kind="captions">
			</video>

			<div class="p-2 flex flex-col shadow-xl rounded-lg">
				<div class="flex">
					<button class="bg-red-400 hover:bg-red-300 text-sm mr-2 px-1 whitespace-nowrap text-white rounded-xl" on:click={() => {set_file = null; time_now = 0;}}>
						Удалить проект
					</button>
					<!-- <button on:click={create_audio} class="btn-blue mx-1 my-1">сгенерить аудио</button> -->
					{#if paused}
						<button class="btn-blue" on:click={() => {paused=false}}>play</button>
					{:else}
						<button class="btn-blue" on:click={() => {paused=true}}>stop</button>
					{/if}
				</div>


				
				
				{#if point_voc[time_now - (time_now % 1)]}
					<div class="border mt-2 p-1 rounded-lg flex flex-col">
						<p class="text-xs text-gray-400 text-center">Настройка отметки(?)</p>
						<div class="flex">
							<p class="mr-1 text-gray-600 text-sm my-auto">Название - </p>
							<input class="p-0.5 rounded-lg" type="text" bind:value={point_voc[time_now - (time_now % 1)].name}>
						</div>


						{#if point_voc[time_now - (time_now % 1)].audio_blob !== null}

							<div class="flex h-20">
								<audio class="my-auto" src={URL.createObjectURL(point_voc[time_now - (time_now % 1)].audio_blob)} controls></audio>
								<button class="bg-red-400 hover:bg-red-300 w-8 h-8 my-auto ml-2 rounded-xl" on:click={() => {point_voc[time_now - (time_now % 1)].audio_blob = null}}>
									<svg width="16" height="16" class="m-auto" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
										<path d="M0.472396 0.472518C0.758152 0.186848 1.14567 0.0263672 1.54973 0.0263672C1.95379 0.0263672 2.34131 0.186848 2.62706 0.472518L8.01525 5.86071L13.4034 0.472518C13.6908 0.194944 14.0758 0.0413523 14.4753 0.0448241C14.8748 0.048296 15.257 0.208553 15.5395 0.49108C15.8221 0.773607 15.9823 1.1558 15.9858 1.55534C15.9893 1.95487 15.8357 2.33979 15.5581 2.62718L10.1699 8.01537L15.5581 13.4036C15.8357 13.691 15.9893 14.0759 15.9858 14.4754C15.9823 14.875 15.8221 15.2571 15.5395 15.5397C15.257 15.8222 14.8748 15.9825 14.4753 15.9859C14.0758 15.9894 13.6908 15.8358 13.4034 15.5582L8.01525 10.17L2.62706 15.5582C2.33967 15.8358 1.95475 15.9894 1.55521 15.9859C1.15568 15.9825 0.773485 15.8222 0.490958 15.5397C0.208431 15.2571 0.048174 14.875 0.0447021 14.4754C0.0412302 14.0759 0.194822 13.691 0.472396 13.4036L5.86059 8.01537L0.472396 2.62718C0.186726 2.34143 0.0262451 1.95391 0.0262451 1.54985C0.0262451 1.14579 0.186726 0.758274 0.472396 0.472518Z" fill="#ffffff"/>
									</svg>
								</button>
							</div>

						{:else}
							{#if !recording_state}
								<button class="btn-blue mt-2 mx-auto" on:click={() => start_recording(time_now)}>Создание аудио дорожки</button>
							{:else}
								<button class="btn-blue mt-2 mx-auto" on:click={stop_recording}>Остановить запись</button>
							{/if}
						{/if}

					</div>
				{:else}
					<button on:click={() => new_poin(time_now)} class="btn-blue mt-2 mx-auto">Создать отметку(?)</button>
				{/if}
			</div>
		</div>

			




		<div class="flex flex-col shadow-xl mt-2 pb-2 rounded-lg">


			
			<p class="text-center my-1">{format(time_now)} / {format(duration)}</p>

			<div class="flex px-4 text-lg">
				<div class="w-full mx-4 my-auto bg-gray-200 rounded-full h-2.5 dark:bg-gray-700"
				on:mousemove={handleMove}
				on:touchmove|preventDefault={handleMove}
				on:mousedown={handleMousedown}
				on:mouseup={handleMouseup}>
					<div class="bg-blue-600 h-2.5 rounded-full" style={"width: " + ((time_now / duration) * 100) + "%;"}></div>
				</div>	
			</div>

			<div class="flex px-4 mt-1 mb-4 text-lg bg-blue-100">
				<div class="flex mx-4 w-full relative bg-green-100 ">
					{#each point_list as point}
						<div class="w-2 h-2 bg-red-600 absolute cursor-pointer rounded-full" on:click={() => time_now = point} style={"left: calc(" + ((point / duration) * 100) + "% - 8px);"}></div>
					{/each}
				</div>
			</div>

			<div class="mx-8" id="waveform"></div>

			<!-- {#if paused} -->

			<!-- {/if} -->

		</div>`

	{/if}

</div>