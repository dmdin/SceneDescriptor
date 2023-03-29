<script lang="ts">
  import {CUTTER_URL} from "$lib/constants";
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();
  
  let set_file: any = null;
  let new_project_name: string = "";
  let saving_state = false;
  async function save_project(){
    saving_state = true;
    let formData = new FormData(); 
    formData.append("file", set_file[0]);
    formData.append("name", new_project_name);
    let out = await postProject(formData)
    console.log(out);
    if(out.state){
      saving_state = false
      set_file = null;
      dispatch("success_creation");
    } 
  }
  
  export async function postProject(formData: any) {
    const response = await fetch(
      CUTTER_URL + "create_project",
      { 
        method: "POST",
        headers: { 
          Accept: "application/json", 
        },
        body: formData
      }
    );
    if(response.ok === true){
      const data = await response.json();
      let out = {state: true, data: data};
      return out;
    } else {
      const data = await response.json();
      let out = {state: false, data: data};
      return out;
    }
  }


</script>

<input accept=".mov, .mp4" hidden id="files" type="file" bind:files={set_file}>

{#if set_file !== null}
    <label for="files" class="w-80 cursor-pointer flex flex-col shadow-xl rounded-xl m-auto m border-2 border-gray-500 hover:border-orange-600">
      
      <p class="text-center font-semibold text-xl text-gray-500 mt-8">Создать новый проект</p>
      <svg width="18" height="18" class="w-14 h-14 mx-auto my-6 cursor-pointer" viewBox="0 0 18 18" fill="none"
            xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd" clip-rule="evenodd"
              d="M12 2H6C3.79086 2 2 3.79086 2 6V12C2 14.2091 3.79086 16 6 16H12C14.2091 16 16 14.2091 16 12V6C16 3.79086 14.2091 2 12 2ZM6 0C2.68629 0 0 2.68629 0 6V12C0 15.3137 2.68629 18 6 18H12C15.3137 18 18 15.3137 18 12V6C18 2.68629 15.3137 0 12 0H6Z"
              fill="#6b7280"/>
        <path
          d="M8.10039 4.9501C8.10039 5.69568 7.49598 6.3001 6.75039 6.3001C6.00481 6.3001 5.40039 5.69568 5.40039 4.9501C5.40039 4.20451 6.00481 3.6001 6.75039 3.6001C7.49598 3.6001 8.10039 4.20451 8.10039 4.9501Z"
          fill="#6b7280"/>
        <path fill-rule="evenodd" clip-rule="evenodd"
              d="M11.8242 7.38837L16.2683 14.0546L17.9324 12.9452L13.0104 5.56209C12.3715 4.60379 10.9357 4.69317 10.4206 5.72332L7.02957 12.5055L5.64629 10.6611C5.0986 9.93085 4.0311 9.85498 3.38563 10.5004L0.193284 13.6928L1.6075 15.107L4.3922 12.3223L5.91498 14.3527C6.58402 15.2447 7.95795 15.1209 8.45662 14.1235L11.8242 7.38837Z"
              fill="#6b7280"/>
      </svg>
    </label>
  {:else}
    <div class="w-80 flex flex-col shadow-xl p-2 rounded-xl m-auto m border-2 border-gray-500"> 
      {#if saving_state}
        <input class="bg-gray-900 border-2 border-gray-700 text-center text-gray-500 focus:border-gray-600 focus:outline-none rounded-xl p-1" type="text" bind:value={new_project_name} placeholder="Введите имя проекта..." name="" id="">
        <video loop style=" 
        object-fit:contain;
        width: 100%;" class="max-h-28 my-2">
          <source src={window.URL.createObjectURL(set_file[0])}>
          <track kind="captions">
        </video>
        <button on:click={save_project} class="text-gray-500 border-2 mx-auto px-2 hover:text-orange-600 hover:border-orange-600 border-gray-500 rounded-xl">
          Сохранить
        </button>
      {:else}
        <p class="text-center font-semibold text-xl text-gray-500 m-8">Проект создается...</p>
      {/if}
    </div>
  {/if}