const apiPrefix = "api/v1"
const logger = document.getElementById('log')
let userToken = 'userToken'

function log(...messages) {
    console.log(...messages)
    logger.innerText += '\n' + messages.map(m => JSON.stringify(m, null, 2)).join(' ')
}

function error(message) {
    console.error(message)
    logger.innerText += '\n' + message
    throw Error('got error:' + message)
}

const asArrayBuffer = v => Uint8Array.from(atob(v.replace(/_/g, '/').replace(/-/g, '+')), c => c.charCodeAt(0))
const asBase64 = ab => btoa(String.fromCharCode(...new Uint8Array(ab)))

async function getPublicKey(path) {
    const r = await fetch(`/${apiPrefix}/${path}`, {
        method: 'GET',
        headers: {'content-type': 'application/json', 'Authorization': `Bearer ${userToken}`}
    })
    if (r.status !== 200) {
        error(`Unexpected response ${r.status}: ${await r.text()}`)
    }
    return await r.json()
}

async function createPublicKey(publicKey, type = 'create') {
    let creds
    try {
        if (type === 'create') {
            creds = await navigator.credentials.create({publicKey})
        } else {
            creds = await navigator.credentials.get({publicKey})
        }
    } catch (err) {
        log('refused:', err.toString())
        return
    }
    return creds
}

async function fidoPost(path, creds, expectedStatus = 201) {
    const {attestationObject, clientDataJSON, signature, authenticatorData} = creds.response
    const data = {
        id: creds.id,
        rawId: asBase64(creds.rawId),
        response: {
            attestationObject: asBase64(attestationObject),
            clientDataJSON: asBase64(clientDataJSON),
        }
    }
    if (signature) {
        data.response.signature = asBase64(signature)
        data.response.authenticatorData = asBase64(authenticatorData)
    }
    const r2 = await fetch(`/${apiPrefix}/${path}`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {'content-type': 'application/json', 'Authorization': `Bearer ${userToken}`}
    })
    if (r2.status !== expectedStatus) {
        error(`Unexpected response ${r2.status}: ${await r2.text()}`)
    }
}

async function fidoRegister() {
    const publicKey = await getPublicKey('authn/register/public_key')
    console.log('register get response:', publicKey)
    publicKey.user.id = asArrayBuffer(publicKey.user.id)
    publicKey.challenge = asArrayBuffer(publicKey.challenge)
    let creds = await createPublicKey(publicKey)
    await fidoPost('authn/register', creds)
    log('registration successful')
}

async function fidoAuthenticate() {
    const publicKey = await getPublicKey('authn/auth/public_key')
    console.log('auth get response:', publicKey)
    publicKey.challenge = asArrayBuffer(publicKey.challenge)
    for (let i = 0; i < publicKey.allowCredentials.length; i++) {
        publicKey.allowCredentials[i].id = asArrayBuffer(publicKey.allowCredentials[i].id)
    }
    let creds = await createPublicKey(publicKey, 'get')
    await fidoPost('authn/auth', creds, 200)
    log('authentication successful')
}

async function authRequest(path, data, expectedStatus = 200) {
    const response = await fetch(`/${apiPrefix}/${path}`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {'content-type': 'application/json'}
    })
    if (response.status !== expectedStatus) {
        error(`Unexpected response ${response.status}: ${await response.text()}`)
    }
    return await response.json()
}

async function authRegister() {
    const login = document.getElementById('registerUsername').value
    const password = document.getElementById('registerPassword').value
    const response = await authRequest('auth/signup', {
        username: login,
        password: password,
        email: `${login}@example.com`
    }, 201)
    console.log('auth register response:', response)
    log('registration successful')
}

async function authLogin() {
    const login = document.getElementById('authUsername').value
    const password = document.getElementById('authPassword').value
    const response = await authRequest(`auth/token`, {username: login, password: password})
    console.log('auth login response:', response)
    userToken = response.access_token
    document.getElementById('authn').style.display = 'block'
    log('login successful')
}
