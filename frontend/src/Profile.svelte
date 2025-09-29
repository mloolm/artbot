<script>
    import { navigate } from 'svelte-routing';
    import FormCard from './FormCard.svelte'; 
    import { onMount } from 'svelte';

    
    
    export let id = null;
    
    
    const STORAGE_KEY = 'userProfiles'; 
    let profiles = [];
    let isEditing = !!id; 
    let currentProfileId = null;
    
    
    // Переменные для формы
    let userData = {
        firstName: '',
        lastName: '',
        email: '',
        citizenshipCode: '',
        
        // Мы не bind'им сюда citizenshipInput, управляются внутри FormCard
    };

    onMount(() => {
        loadProfiles();
        // Определяем режим работы
          
    
        if (isEditing) {
            currentProfileId = parseInt(id);

            const profileToEdit = profiles.find(p => p.id === currentProfileId);
            
            if (profileToEdit) {
                
                // Загружаем данные профиля в форму.
                // Присваиваем все свойства объекта userData, включая коды стран
                userData = { ...profileToEdit };
            } else {
                isEditing = false;
                alert('Профиль не найден! Перенаправление на список.');
                navigate('/');
            }
        }
    });

    // --- ЛОГИКА LOCAL STORAGE (скопирована из Profile.svelte) ---

    function loadProfiles() {
        try {
            const storedProfiles = localStorage.getItem(STORAGE_KEY);
            if (storedProfiles) {
                profiles = JSON.parse(storedProfiles);
                console.log(profiles);
            }
        } catch (e) {
            console.error("Ошибка загрузки профилей из localStorage:", e);
        }
    }

    function saveProfiles() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(profiles));
            console.log("Профили успешно сохранены в localStorage.");
        } catch (e) {
            console.error("Ошибка сохранения профилей в localStorage:", e);
        }
    }

    // --- ЛОГИКА TWA ---

    function closeWebApp() {
        if (window.Telegram?.WebApp) {
            window.Telegram.WebApp.close();
        } else {
            console.log("Telegram WebApp не найден. Перенаправление на список.");
            navigate('/');
        }
    }

    // --- ОБРАБОТКА ОТПРАВКИ ФОРМЫ ---
    
    function handleFormSubmit(event) {
        const submittedData = event.detail; 
        let successMessage = '';

        if (isEditing) {
            // РЕЖИМ РЕДАКТИРОВАНИЯ: Находим профиль и обновляем его
            profiles = profiles.map(p => 
                p.id === currentProfileId 
                    ? { ...submittedData, id: currentProfileId, updatedAt: new Date().toISOString() }
                    : p
            );
            successMessage = 'Профиль успешно обновлен!';
        } else {
            // РЕЖИМ ДОБАВЛЕНИЯ: Создаем новый профиль
            const newProfile = {
                id: Date.now(), 
                createdAt: new Date().toISOString(),
                ...submittedData
            };
            profiles = [...profiles, newProfile];
            successMessage = 'Профиль успешно сохранен!';
        }

        saveProfiles();
        // Перенаправляем на главную страницу (список)
        navigate('/');
    }
</script>

<div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md flex flex-col space-y-6 mx-auto mt-10">
    <h2 class="text-xl font-bold text-[#0088cc] border-b pb-4 text-center">
        {isEditing ? 'Редактировать профиль' : 'Добавить новый профиль'}
    </h2>

    <FormCard 
        on:submit={handleFormSubmit} 
        bind:firstName={userData.firstName}
        bind:lastName={userData.lastName}
        bind:email={userData.email}
        bind:citizenshipCode={userData.citizenshipCode}
        
    />
    
    <button
        class="w-full py-2 bg-gray-300 text-gray-700 font-semibold rounded-md transition duration-150 hover:bg-gray-400"
        on:click={() => navigate('/')}
    >
        Отмена (Вернуться к списку)
    </button>
</div>