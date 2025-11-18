def create_sample_presentation():
    return '''
    <div class="presentation-container">
        <div class="slide current-slide" id="slide-1">
            <div class="slide-number">Слайд 1 из 3</div>
            <h2 class="slide-title">Добро пожаловать в систему медицинских продаж!</h2>
            <div class="slide-content">
                <p>Эта система предназначена для управления агентской сетью по продаже медицинского оборудования.</p>
                <p><strong>Основные возможности:</strong></p>
                <ul>
                    <li>Управление агентами и их комиссиями</li>
                    <li>Отслеживание продаж и доходов</li>
                    <li>Обучающие материалы и презентации</li>
                    <li>Аналитика эффективности</li>
                </ul>
            </div>
        </div>

        <div class="slide hidden-slide" id="slide-2">
            <div class="slide-number">Слайд 2 из 3</div>
            <h2 class="slide-title">Медицинское оборудование</h2>
            <div class="slide-content">
                <p>Мы предлагаем широкий спектр медицинского оборудования:</p>
                <ul>
                    <li><strong>Диагностическое оборудование:</strong> ЭКГ, УЗИ, рентген аппараты</li>
                    <li><strong>Терапевтическое оборудование:</strong> Инфузионные помпы, аппараты ИВЛ</li>
                    <li><strong>Реанимационное оборудование:</strong> Дефибрилляторы, мониторы пациента</li>
                </ul>
            </div>
        </div>

        <div class="slide hidden-slide" id="slide-3">
            <div class="slide-number">Слайд 3 из 3</div>
            <h2 class="slide-title">Система комиссий</h2>
            <div class="slide-content">
                <p><strong>Структура комиссий:</strong></p>
                <ul>
                    <li>Базовый процент: 10% от суммы продажи</li>
                    <li>Повышенный процент при объеме продаж более 1 млн руб.: 12%</li>
                    <li>Бонус за постоянных клиентов: +2%</li>
                </ul>
            </div>
        </div>
    </div>

    <style>
        .slide { display: none; padding: 20px; border: 1px solid #ccc; margin: 10px 0; }
        .current-slide { display: block; }
        .slide-number { background: #007bff; color: white; padding: 5px 10px; display: inline-block; }
        .slide-title { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
    </style>

    <script>
        let currentSlide = 1;
        function showSlide(n) {
            document.querySelectorAll('.slide').forEach(slide => slide.classList.remove('current-slide'));
            document.getElementById('slide-' + n).classList.add('current-slide');
        }
        function nextSlide() { if (currentSlide < 3) showSlide(++currentSlide); }
        function prevSlide() { if (currentSlide > 1) showSlide(--currentSlide); }
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
        });
    </script>
    '''