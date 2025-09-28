<script>
  // Используем переменные, которые вы хотите привязать
  let firstName = '';
  let lastName = '';

  // Простая функция-обработчик
  function handleSubmit() {
    alert(`Форма отправлена! Имя: ${firstName}, Фамилия: ${lastName}`);
    // Здесь можно было бы отправить данные на ваш бэкенд
  }
</script>

<div class="card">
  <h2>Заполните свои данные</h2>

  <form on:submit|preventDefault={handleSubmit}>

    <div class="form-group">
      <label for="firstName">Имя</label>
      <input
        id="firstName"
        type="text"
        placeholder="Введите имя"
        bind:value={firstName}
        required
      />
    </div>

    <div class="form-group">
      <label for="lastName">Фамилия</label>
      <input
        id="lastName"
        type="text"
        placeholder="Введите фамилию"
        bind:value={lastName}
        required
      />
    </div>

    <button type="submit" disabled={!firstName || !lastName}>
      Отправить данные
    </button>
  </form>
</div>

