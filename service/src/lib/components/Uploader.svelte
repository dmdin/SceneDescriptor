<script lang="ts">
  import {CUTTER_URL} from "$lib/constants";
  import { createEventDispatcher } from "svelte";
  import {Circle} from "svelte-loading-spinners";

  import {DocumentPlus} from 'svelte-heros-v2'


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
    } else {
      alert("Ошибка, чекни консоль")
      saving_state = false
      set_file = null;
    }
  }
  
  export async function postProject(formData: any) {
    const response = await fetch(
      CUTTER_URL + "create_project/",
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

{#if set_file === null}
    <label for="files" class="cursor-pointer p-4 flex flex-col shadow-xl rounded-xl m-auto border-2 border-gray-500 hover:border-orange-600">
      <p class="text-center font-semibold text-xl text-gray-500 mt-8">Создать новый проект</p>
      <DocumentPlus class="w-14 h-14 mx-auto my-6" variation="solid" color="#6b7280"/>
    </label>
  {:else}
    <div class="w-80 flex flex-col shadow-xl p-4 rounded-xl m-auto border-2 border-gray-500"> 
      {#if !saving_state}

        <input class="bg-gray-900 border-2 text-sm border-gray-700 text-gray-300 text-center placeholder:text-gray-500 focus:border-gray-600 focus:outline-none rounded-xl p-1" type="text" bind:value={new_project_name} placeholder="Введите имя проекта..." name="" id="">

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
        <p class="text-center font-semibold text-xl text-gray-500 m-6 mb-4">Проект создается...</p>
        <div class="mx-auto">
          <Circle size="40"  color="#FF3E00" unit="px" duration="1s"/>
        </div>
        
      {/if}
    </div>
  {/if}