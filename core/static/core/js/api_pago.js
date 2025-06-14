import cl.transbank.webpay.webpayplus.WebpayPlus;
import cl.transbank.webpay.webpayplus.model.TransactionCreateResponse;

public class WebpayExample {

    public static void main(String[] args) {
        try {
            // Datos de prueba (modo integración)
            String buyOrder = "orden123456";
            String sessionId = "sesion123456";
            double amount = 10000;
            String returnUrl = "https://www.tuapp.cl/webpay/retorno";

            TransactionCreateResponse response = WebpayPlus.Transaction.create(
                buyOrder,
                sessionId,
                amount,
                returnUrl
            );

            System.out.println("URL para redirigir al cliente: " + response.getUrl());
            System.out.println("Token: " + response.getToken());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}