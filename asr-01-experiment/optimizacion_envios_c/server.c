#include <microhttpd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define PORT 3000

enum MHD_Result request_handler(void *cls, struct MHD_Connection *connection,
                                const char *url, const char *method,
                                const char *version, const char *upload_data,
                                size_t *upload_data_size, void **con_cls) {
    (void)cls; (void)version; (void)upload_data; (void)upload_data_size; (void)con_cls;

    const char *response_text;
    if (strcmp(url, "/optimizacion_envios") == 0) {
        response_text = "{ \"altitude\": 15.2, \"latitude\": 37.7749, \"longitude\": -122.4194, \"coordinate_system\": \"C - Delivery optimization service\" }";
    } else {
        response_text = "Hello from C!";
    }

    struct MHD_Response *response = MHD_create_response_from_buffer(strlen(response_text),
                                                                    (void *)response_text,
                                                                    MHD_RESPMEM_PERSISTENT);
    if (!response)
        return MHD_NO;

    MHD_add_response_header(response, "Content-Type", "application/json");

    int ret = MHD_queue_response(connection, MHD_HTTP_OK, response);
    MHD_destroy_response(response);

    return ret;
}

int main() {
    struct MHD_Daemon *server = MHD_start_daemon(MHD_USE_THREAD_PER_CONNECTION, PORT, NULL, NULL,
                                                 &request_handler, NULL, MHD_OPTION_END);
    if (!server) {
        printf("Failed to start server.\n");
        return 1;
    }

    printf("Server is running on http://localhost:%d\n", PORT);
    while (1) {
        sleep(1);
    }

    MHD_stop_daemon(server);
    return 0;
}
