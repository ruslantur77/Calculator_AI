document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', async (e) => {
        e.preventDefault();
        
        const num1 = document.getElementById('first_number').value;
        const num2 = document.getElementById('second_number').value;
        const operation = e.target.classList[0];

        try {
            const response = await fetch('/Calc', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    num1: num1,
                    num2: num2,
                    operation: operation
                })
            });

            const data = await response.json();
            if(data.error) throw new Error(data.error);
            
            document.getElementById('result').innerHTML = `
                Предсказанный результат: ${data.predicted.toFixed(3)}<br>
                Реальное значение: ${data.real}<br>
                Предсказанный отличается от реального на:  ${(Math.abs((data.real - data.predicted)/data.predicted * 100)).toFixed(3)} %
            `;
        } catch (error) {
            document.getElementById('result').innerHTML = 
                `Ошибка: ${error.message}`;
        }
    });
});

