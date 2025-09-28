<script>
  import { navigate } from 'svelte-routing';

  let firstName = '';
  let lastName = '';

  // Функция для закрытия WebApp
  function closeWebApp() {
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.close();
    } else {
      console.log("Telegram WebApp не найден. Перенаправление на главную.");
      navigate('/'); // Для отладки в браузере
    }
  }

  function handleSubmit() {
    alert(`Форма отправлена! Имя: ${firstName}, Фамилия: ${lastName}`);
    // Здесь можно отправить данные на бэкенд, а затем закрыть приложение:
    // closeWebApp();
  }
</script>

<div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md flex flex-col space-y-6">
  <h2 class="text-xl font-bold text-[#0088cc] border-b pb-4 text-center">
    Заполните профиль
  </h2>

  <form on:submit|preventDefault={handleSubmit} class="space-y-4">

    <div class="space-y-1">
      <label for="firstName" class="block font-medium text-gray-700">Имя</label>
      <input
        id="firstName"
        type="text"
        placeholder="Введите имя"
        bind:value={firstName}
        required
        class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0088cc] focus:border-[#0088cc]"
      />
    </div>

    <div class="space-y-1">
      <label for="lastName" class="block font-medium text-gray-700">Фамилия</label>
      <input
        id="lastName"
        type="text"
        placeholder="Введите фамилию"
        bind:value={lastName}
        required
        class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0088cc] focus:border-[#0088cc]"
      />
    </div>

    <button
      type="submit"
      disabled={!firstName || !lastName}
      class="w-full py-2 bg-[#0088cc] text-white font-semibold rounded-md transition duration-150 hover:bg-[#0066a3] disabled:bg-gray-400 disabled:cursor-not-allowed"
    >
      Сохранить и закрыть
    </button>
  </form>

  <button
    class="w-full py-2 bg-gray-300 text-gray-700 font-semibold rounded-md transition duration-150 hover:bg-gray-400"
    on:click={closeWebApp}
  >
    Отмена (Закрыть WebApp)
  </button>
</div>

