<script>
  import { onMount } from "svelte";
  import { Router, Route, navigate } from "svelte-routing";
  import ProfileList from '../components/ProfileList.svelte';      // компонент для списка
  import ProfileFormPage from './Profile.svelte'; // компонент для формы профиля
  import Letter from './Letter.svelte'; //компонент формы для формирования письма
  import './app.css';

  let user = 0;
  let is_inside_telegram = false;  
  onMount(() => {
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready();
      if(typeof tg.initDataUnsafe.user !== 'undefined')
      {
        user = tg.initDataUnsafe.user;
      }
      
      if(user)
      {
        is_inside_telegram = true;
      }
      is_inside_telegram = true;
    }
  });

  // Перенаправляет на страницу добавления профиля
  function goToProfileAddPage() {
      navigate('/profile/add');
  }

  function closeApp(){
    if(is_inside_telegram)
    {
         window.Telegram.WebApp.close(); 
    }
  }
</script>

<main class="min-h-screen bg-gray-100 p-6 flex flex-col items-center justify-start space-y-6">
  <Router>
    <Route path="/">
        <h2 class="text-1xl font-semibold text-[#0088cc] text-center">
            Делаем разрешение на вывоз произведений искусства из Грузии
        </h2>
        
        <ProfileList />

        <button
            class="px-6 py-3 mt-4 bg-[#0088cc] text-white font-semibold rounded-xl shadow-md transition duration-200 hover:bg-[#0066a3] focus:outline-none focus:ring-4 focus:ring-[#0088cc]/50"
            on:click={goToProfileAddPage}
        >
            Добавить новый профиль
        </button>


        {#if is_inside_telegram}
            <div class="mt-5 pt-5">
                <button
                    on:click={closeApp} 
                    class="px-6 py-3 text-gray rounded-xl bg-[#999999]"
                >Выйти и вернуться в bot</button>
            </div>
        {/if}    

    </Route>

     <Route path="/profile/add">
        <ProfileFormPage />
    </Route>

    <Route path="/profile/edit/:id" let:params>
        <ProfileFormPage id={params.id} />
    </Route>

     <Route path="/letter/:id" let:params>
        <Letter id={params.id} />
    </Route>
  </Router>
</main>