<script>
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
    import LetterForm from '../components/LetterForm.svelte';

    // Принимаем ID профиля из роута
    export let id = null; 

    const STORAGE_KEY = 'userProfiles'; 
    let profile = null;
    
    // Переменные для формы LetterForm
    let formState = {
        countryToInput: '', 
        countryToCode: '', 
        items: []
    };

    onMount(() => {
        if (id) {
            const profiles = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
            const foundProfile = profiles.find(p => p.id === parseInt(id));
            
            if (foundProfile) {
                profile = foundProfile;
            } else {
                alert('Профиль не найден! Возврат к списку.');
                navigate('/');
            }
        } else {
            alert('Не указан ID профиля! Возврат к списку.');
            navigate('/');
        }
    });

    function handleLetterSubmit(event) {
        const { countryToCode, countryToValue, items: formItems } = event.detail;

        if (!profile) return;

        // Собираем финальную структуру
        const finalData = {
            // Данные из профиля (citizenshipValue был 4-й столбец)
            first_name: profile.firstName,
            last_name: profile.lastName,
            email: profile.email,
            citizenship: profile.citizenshipValue, // Используем значение 4-го столбца

            // Данные из LetterForm (countryToValue был 5-й столбец)
            country_to: countryToValue, 

            // Список работ
            items: formItems 
        };

        console.log("Финальная структура для отправки/генерации:", finalData);

        alert(`Письмо сгенерировано! Гражданство: ${finalData.citizenship}, Назначение: ${finalData.country_to}, Работ: ${finalData.items.length}`);
        
        // Здесь можно отправить finalData на бэкенд или в логику генерации PDF
    }
</script>

<div class="max-w-md mx-auto p-6 bg-gray-100 flex flex-col space-y-6 mt-10">
    <h2 class="text-2xl font-bold text-[#0088cc] border-b pb-4 text-center">
        Генерация письма
    </h2>

    {#if profile}
        <div class="p-3 bg-blue-100 border border-blue-300 rounded-lg text-sm">
            <p><strong>Профиль:</strong> {profile.firstName} {profile.lastName}</p>
            <p><strong>Гражданство (Value):</strong> {profile.citizenshipValue}</p>
        </div>
        
        <LetterForm 
            on:submit={handleLetterSubmit} 
            bind:countryToInput={formState.countryToInput}
            bind:countryToCode={formState.countryToCode}
            bind:items={formState.items}
        />
    {:else}
        <div class="p-4 bg-yellow-100 text-yellow-800 rounded-lg text-center">Загрузка профиля...</div>
    {/if}

    <button
        class="w-full py-2 bg-gray-300 text-gray-700 font-semibold rounded-md transition duration-150 hover:bg-gray-400"
        on:click={() => navigate('/')}
    >
        Отмена
    </button>
</div>