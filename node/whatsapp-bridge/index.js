// Bot de WhatsApp con DEBUG INTENSIVO
const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');
const axios = require('axios');
const fs = require('fs');

// ================= CONFIGURACIÓN ================= //
const CONFIG = {
    FASTAPI_URL: 'http://localhost:8000',
    SESSION_PATH: './whatsapp-session'
};

// Crear directorio de sesión
if (!fs.existsSync(CONFIG.SESSION_PATH)) {
    fs.mkdirSync(CONFIG.SESSION_PATH, { recursive: true });
}

// ================= CLIENTE WHATSAPP ================= //
const client = new Client({
    authStrategy: new LocalAuth({
        clientId: "debug-bot",
        dataPath: CONFIG.SESSION_PATH
    }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// ================= LOGGING DETALLADO ================= //
function debugLog(emoji, title, data = null) {
    const timestamp = new Date().toISOString();
    console.log(`\n${emoji} [${timestamp}] ${title}`);
    if (data) {
        console.log('📋 Datos:', JSON.stringify(data, null, 2));
    }
    console.log('─'.repeat(50));
}

// ================= FUNCIÓN PARA ENVIAR A FASTAPI ================= //
async function sendToFastAPI(messageText) {
    debugLog('🚀', `ENVIANDO A FASTAPI: "${messageText}"`);
    
    try {
        const requestData = { text: messageText };
        debugLog('📤', 'REQUEST A FASTAPI', requestData);
        
        const response = await axios.post(`${CONFIG.FASTAPI_URL}/chat`, requestData, {
            timeout: 10000,
            headers: { 'Content-Type': 'application/json' }
        });
        
        debugLog('✅', 'RESPUESTA DE FASTAPI RECIBIDA');
        debugLog('📊', 'STATUS HTTP', response.status);
        debugLog('📄', 'HEADERS', response.headers);
        debugLog('📋', 'DATA COMPLETA', response.data);
        
        if (response.data && response.data.response) {
            const botResponse = response.data.response;
            debugLog('🎯', `RESPUESTA EXTRAÍDA: "${botResponse}"`);
            return botResponse;
        } else {
            debugLog('❌', 'FORMATO DE RESPUESTA INVÁLIDO');
            return 'Error: Respuesta inválida del servidor';
        }
        
    } catch (error) {
        debugLog('💥', 'ERROR EN FASTAPI', {
            message: error.message,
            status: error.response?.status,
            data: error.response?.data
        });
        return 'Error: No se pudo conectar con el servidor';
    }
}

// ================= EVENTOS DEL CLIENTE ================= //
client.on('qr', (qr) => {
    debugLog('📱', 'CÓDIGO QR GENERADO');
    qrcode.generate(qr, { small: true });
    console.log('\n⏰ Escanea el código QR con WhatsApp\n');
});

client.on('ready', async () => {
    debugLog('✅', 'BOT CONECTADO Y LISTO');
    
    // Prueba FastAPI inmediatamente
    debugLog('🔬', 'PROBANDO CONEXIÓN CON FASTAPI');
    const testResponse = await sendToFastAPI('test de conexión');
    debugLog('🧪', `RESULTADO DE PRUEBA: "${testResponse}"`);
});

client.on('authenticated', () => {
    debugLog('🔐', 'AUTENTICADO CON WHATSAPP');
});

// ================= MANEJO DE MENSAJES CON DEBUG ================= //
client.on('message', async (message) => {
    try {
        debugLog('📨', 'NUEVO MENSAJE RECIBIDO');
        
        // Información básica del mensaje
        debugLog('📍', 'INFO DEL MENSAJE', {
            fromMe: message.fromMe,
            body: message.body,
            from: message.from,
            to: message.to,
            type: message.type,
            timestamp: message.timestamp
        });
        
        // Ignorar mensajes propios
        if (message.fromMe) {
            debugLog('⏭️', 'MENSAJE PROPIO - IGNORADO');
            return;
        }
        
        // Obtener chat y contacto
        const chat = await message.getChat();
        const contact = await message.getContact();
        
        debugLog('👤', 'INFO DEL CONTACTO', {
            name: contact.name,
            number: contact.number,
            isGroup: chat.isGroup,
            chatName: chat.name
        });
        
        // Ignorar grupos (opcional)
        if (chat.isGroup) {
            debugLog('👥', 'MENSAJE DE GRUPO - IGNORADO');
            return;
        }
        
        const messageText = message.body?.trim() || '';
        
        if (!messageText) {
            debugLog('⚠️', 'MENSAJE VACÍO');
            await message.reply('Por favor envía un mensaje con texto 📝');
            debugLog('✅', 'RESPUESTA A MENSAJE VACÍO ENVIADA');
            return;
        }
        
        debugLog('💬', `PROCESANDO MENSAJE: "${messageText}"`);
        
        // Comando de prueba rápida
        if (messageText.toLowerCase() === '/test') {
            debugLog('🧪', 'COMANDO DE PRUEBA DETECTADO');
            const testMessage = await message.reply('🤖 ¡Bot funcionando correctamente!');
            debugLog('✅', 'MENSAJE DE PRUEBA ENVIADO', {
                messageId: testMessage.id._serialized,
                success: !!testMessage
            });
            return;
        }
        
        // Mostrar "escribiendo"
        debugLog('⌨️', 'ENVIANDO INDICADOR DE ESCRITURA');
        await chat.sendStateTyping();
        
        // PASO CRÍTICO: Enviar a FastAPI
        debugLog('🔄', 'INICIANDO COMUNICACIÓN CON FASTAPI');
        const botResponse = await sendToFastAPI(messageText);
        debugLog('🎯', `RESPUESTA OBTENIDA DE FASTAPI: "${botResponse}"`);
        
        if (!botResponse) {
            debugLog('❌', 'NO SE OBTUVO RESPUESTA DE FASTAPI');
            return;
        }
        
        // PASO CRÍTICO: Enviar respuesta a WhatsApp
        debugLog('📤', 'ENVIANDO RESPUESTA A WHATSAPP');
        debugLog('📝', `TEXTO A ENVIAR: "${botResponse}"`);
        
        const sentMessage = await message.reply(botResponse);
        
        // Verificar envío exitoso
        if (sentMessage) {
            debugLog('🎉', 'MENSAJE ENVIADO EXITOSAMENTE', {
                messageId: sentMessage.id._serialized,
                to: sentMessage.to,
                body: sentMessage.body,
                timestamp: sentMessage.timestamp
            });
        } else {
            debugLog('💀', 'ERROR: NO SE PUDO ENVIAR EL MENSAJE');
        }
        
    } catch (error) {
        debugLog('💥', 'ERROR CRÍTICO EN MANEJO DE MENSAJE', {
            message: error.message,
            stack: error.stack
        });
        
        try {
            await message.reply('❌ Error interno. Intenta nuevamente.');
            debugLog('🚨', 'MENSAJE DE ERROR ENVIADO');
        } catch (replyError) {
            debugLog('💀', 'ERROR ENVIANDO MENSAJE DE ERROR', replyError.message);
        }
    }
});

// Evento para confirmar cuando se crean mensajes
client.on('message_create', (message) => {
    if (message.fromMe && message.body) {
        debugLog('📤', 'MENSAJE CREADO POR EL BOT', {
            body: message.body,
            to: message.to,
            id: message.id._serialized
        });
    }
});

// Evento para seguimiento de entrega
client.on('message_ack', (message, ack) => {
    if (message.fromMe && message.body) {
        const ackStatus = {
            1: 'Enviado al servidor',
            2: 'Entregado al dispositivo',
            3: 'Leído por el usuario'
        };
        debugLog('📨', `ESTADO DEL MENSAJE: ${ackStatus[ack] || `Desconocido (${ack})`}`, {
            messageBody: message.body.substring(0, 50),
            ack: ack
        });
    }
});

// ================= MANEJO DE ERRORES ================= //
process.on('unhandledRejection', (error) => {
    debugLog('💥', 'ERROR NO MANEJADO', error.message);
});

// ================= INICIALIZACIÓN ================= //
debugLog('🚀', 'INICIANDO BOT DE WHATSAPP CON DEBUG');
debugLog('🔗', `FASTAPI URL: ${CONFIG.FASTAPI_URL}`);

client.initialize().catch(error => {
    debugLog('💀', 'ERROR FATAL EN INICIALIZACIÓN', error.message);
    process.exit(1);
});