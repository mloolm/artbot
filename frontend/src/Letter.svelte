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


// 🔥 ВАЖНО: Получаем базовый URL из переменных окружения
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

let IS_TWA = false;
if(typeof window.Telegram != 'undefined')
{
    if(typeof window.Telegram.WebApp != 'undefined')
    {
        IS_TWA = true;
    }
    
}

const telegramUserId = IS_TWA ? parseInt(window.Telegram.WebApp.initDataUnsafe?.user?.id) : 0;


// --- ФУНКЦИЯ: ОТПРАВКА ДАННЫХ И ПОЛУЧЕНИЕ JSON-СТАТУСА ---
async function postLetterData(data) {
    if (!API_BASE_URL) {
        console.error("Ошибка: VITE_API_BASE_URL не определен в переменных окружения.");
        alert("Ошибка конфигурации: Базовый URL API не найден.");
        return;
    }
    
    const fullUrl = `${API_BASE_URL}/letter/`;

    // Добавляем метаданные для бэкенда
    const dataToSend = {
        ...data,
        is_twa: IS_TWA,
        telegram_user_id: telegramUserId 
    };


    try {
        const response = await fetch(fullUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataToSend),
        });

        
        
        if (IS_TWA) {
            // 🔥 РЕЖИМ TWA: Ожидаем JSON-статус. Бэкенд сам отправил файл в чат.
            const result = await response.json(); 
            
            console.log("Успешный TWA-ответ:", result);
            alert(`Письмо сгенерировано! ${result.message || 'Проверьте чат Telegram.'}`);
            
            // Опционально: закрываем TWA
            // window.Telegram.WebApp.close(); 

        } else {
            alert('sss');
            // 🔥 РЕЖИМ БРАУЗЕРА: Ожидаем бинарный файл (PDF Blob) и скачиваем его.
            
            // 1. Получаем Blob
            const blob = await response.blob(); 
            
            // 2. Определяем имя файла
            let filename = 'application_letter.pdf'; // Имя по умолчанию
            const disposition = response.headers.get('Content-Disposition');
            // ... (логика определения filename по Content-Disposition) ...
            if (disposition && disposition.indexOf('attachment') !== -1) {
                const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                const matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, '').trim();
                }
            }
            
            // 3. Создаем URL, ссылку и запускаем скачивание
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename; 
            
            document.body.appendChild(a);
            a.click();
            
            a.remove();
            window.URL.revokeObjectURL(url);

            console.log(`Файл ${filename} успешно загружен в браузере.`);
            alert("Письмо успешно сгенерировано и скачано.");
        }

    } catch (error) {
        console.error("Ошибка при отправке данных на бэкенд:", error);
        alert(`Не удалось сгенерировать письмо. Ошибка: ${error.message}`);
    }
}


    function handleLetterSubmit(event) {
    const { countryToCode, countryToValue, items: formItems } = event.detail;

    if (!profile) return;

    // 1. Собираем финальную структуру
    const finalData = {
        first_name: profile.firstName,
        last_name: profile.lastName,
        email: profile.email,
        citizenship: profile.citizenshipValue,
        country_to: countryToValue, 
        items: formItems 
    };

    console.log("Финальная структура для отправки:", finalData);
    
    // 2. Отправляем данные на бэкенд
    // Оборачиваем в .catch, если не хотим делать handleLetterSubmit асинхронным
    postLetterData(finalData); 
    
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