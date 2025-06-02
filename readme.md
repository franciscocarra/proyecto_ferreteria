# 🛠 Ferretería Online

¡Bienvenido a la web de Ferretería Online! Aquí podrás encontrar una amplia variedad de productos y gestionar compras de manera sencilla y segura.

---

## 📄 Descripción

Este proyecto es una página web desarrollada en HTML5 que ofrece funcionalidades básicas para un e-commerce de ferretería. Los usuarios pueden navegar entre productos, gestionar su perfil, realizar compras y consultar precios actualizados en dólares.

La aplicación cuenta con:

- 🛒 Catálogo de productos  
- 👤 Gestión de usuarios  
- 💲 Conversión automática de precios a dólares  
- 💳 Procesamiento de pagos  

---

## ⚙ Tecnologías utilizadas

| Tecnología | Descripción |
|------------|-------------|
| HTML5  | Lenguaje de marcado principal para la estructura y el contenido de la web. |
| CSS3   | Para dar estilo y diseño a la página (no mencionado explícitamente, pero se asume para la presentación visual). |
| Python | Usado para validar formularios y datos en el backend, además de la creación de la API de productos. |
| FastAPI| Framework en Python para crear la API REST que gestiona el catálogo de productos. |
| Java   | Utilizado con Express para crear la API de usuarios (personas). (Nota: normalmente Express es para JavaScript/Node.js, pero aquí lo mencionas con Java, así que lo dejo así). |
| APIs externas |  
  - API de pago: Para procesar los pagos en línea.  
  - API de conversión de divisas: Para convertir precios a dólares automáticamente. |

---

## 🔌 Validaciones

El backend en Python realiza las siguientes validaciones:

✅ Validación de datos en formularios de contacto y compra.  
✅ Validación de datos ingresados para la creación/actualización de productos.  
✅ Validación de usuarios para el acceso y creación de perfiles.

---

## 🔗 APIs

### 🌐 API interna de productos (FastAPI en Python)

- 📦 Gestiona el catálogo de productos: creación, actualización, listado y eliminación.  
- 📥 Devuelve la lista de productos actualizada en tiempo real.  

### 🌐 API interna de usuarios (Express en Java)

- 👤 Gestiona los perfiles de usuario (registro, login y actualizaciones).  
- 🔐 Maneja la autenticación y autorización de usuarios.
 
### 💻 instalación
- git clone (url) 
- npm init -y
- npm install cors

- pyp install cors

### Planes a futuro 📲

1️⃣ API de pago: Integra métodos de pago confiables para procesar transacciones seguras.  
2️⃣ API de conversión a dólar: Convierte los precios de los productos automáticamente a dólares utilizando tasas de cambio en tiempo real.

###Importante ⚠
- Esta pagina solo ingresa datos de momento