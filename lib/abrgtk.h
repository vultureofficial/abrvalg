#include <gtk/gtk.h>
#include <data_types.h>

// int
// main (int    argc,
//       char **argv)
// {
//   GtkApplication *app;
//   int status;

//   app = gtk_application_new ("org.gtk.example", G_APPLICATION_FLAGS_NONE);
//   g_signal_connect (app, "activate", G_CALLBACK (activate), NULL);
//   status = g_application_run (G_APPLICATION (app), argc, argv);
//   g_object_unref (app);

//   return status;
// }

class abrgtk {
    public:
    gtk() {}
    ~gtk() {}

    GtkApplication * application_new(string package) {
        GtkApplication * app = gtk_application_new (package.c_str(), G_APPLICATION_FLAGS_NONE);
        return app; 
    }

    void signal_connect (GtkAppliaction *app ,string envt, void (*fx) (auto, auto)) {
        g_signal_connect (app, envt.c_str(), G_CALLBACK (fx), NULL);
    }

    void object_unref (GtkApplication *app) {
        g_object_unref (app);
    }

    i32 application_run (GtkApplication *app) {
        i32 argc = 0; 
        char ** argv = {"app"};
        i32 status = g_application_run (G_APPLICATION (app), argc, argv);
        return status; 
    }

    GtkWidget* application_window_new(GtkApplication *app) {
        GtkWidget *window;
        window = gtk_application_window_new (app);
        return window; 
    }

    void window_set_title(GtkWidget *window, string title) {
        gtk_window_set_title (GTK_WINDOW (window), title.c_str());
    }

    void window_set_default_size(GtkWidget *window, i32 width, i32 height) {
        gtk_window_set_default_size (GTK_WINDOW (window), width, height); 
    }

    void widget_show_all(GtkWidget *window) {
        gtk_widget_show_all (window);
    }

    
}
