<script>
  import { onMount } from "svelte";
  // 💥 Импорт компонентов маршрутизации
  import { Router, Route, navigate } from "svelte-routing";
  import AddProfile from './AddProfile.svelte';
  import './app.css';
  let user = null;

  onMount(() => {

    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready();
      user = tg.initDataUnsafe?.user;
    }
  });

  function goToProfilePage() {
      navigate('/add-profile');
  }
</script>

<main class="min-h-screen bg-gray-100 p-6 flex flex-col items-center justify-start space-y-6">
  <Router>
    <Route path="/">

      <h1 class="text-3xl font-extrabold text-[#0088cc] text-center">
        Привет из Telegram WebApp 🚀
      </h1>

      {#if user}
        <p class="p-3 bg-blue-100 text-blue-800 rounded-lg font-semibold text-center shadow-sm">
          Ты зашёл как: **{user.first_name} {user.last_name}**
        </p>
      {:else}
         <p class="p-3 bg-yellow-100 text-yellow-800 rounded-lg font-medium text-center shadow-sm">
           Данные пользователя не загружены.
         </p>
      {/if}

      <button
        class="px-6 py-3 mt-4 bg-[#0088cc] text-white font-semibold rounded-xl shadow-md transition duration-200 hover:bg-[#0066a3] focus:outline-none focus:ring-4 focus:ring-[#0088cc]/50"
        on:click={goToProfilePage}
      >
        Перейти к заполнению профиля
      </button>

    </Route>

    <Route path="/add-profile" component={AddProfile} />
  </Router>
</main>
