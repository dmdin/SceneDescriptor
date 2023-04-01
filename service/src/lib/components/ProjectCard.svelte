<script lang="ts">
  import {goto} from "$app/navigation";

  export let description
  export let video
  export let preview
  export let audio
  export let name: string
  export let id

  export let textCls = 'text-xl'
  function open_project(){
    if(navigator.userAgent.indexOf('Chrome') !== -1){
      alert("Некоторый функционал сайта может работать нестабильно в браузере Google Chrome, пожалуйста, попробуйте открыть сайт с другого браузера.")
    }
    // window.history.replaceState(history.state, '', `/manual_editor/${id}`)

    goto(`/manual_editor/${id}`, { replaceState: true })
    // location.reload()
  }
</script>

<a href="/manual_editor/{id}">
<div class="{$$props.class} bg-gray-900  h-full flex flex-col rounded-lg shadow border-2 border-gray-500 border-transparent transition-colors hover:border-orange-600 cursor-pointer"
  on:click={open_project}
>
  <img class="rounded-t-lg my-auto" src={preview} alt="Preview"/>

  <div class="p-2 mt-auto">
    <p class="mb-1 {textCls} font-normal text-center tracking-tight text-gray-500">{name}</p>
  </div>
</div>
</a>