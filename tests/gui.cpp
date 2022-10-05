#include <data_types.h>
#include <vector>
#include <range.h>


#include <abrgtk.h>
void activate(auto app, auto data) {
auto window = abrgtk().application_window_new (app);;
abrgtk().window_set_title (window , "Testing");
abrgtk().window_set_default_size (window , 200 , 200);
abrgtk().widget_show_all (window);
return ;
}

i32 main() {
auto app = abrgtk().application_new ("com.application.new");;
abrgtk().signal_connect (app , "activate" , activate);
i32 status = abrgtk().application_run (app);;
abrgtk().object_unref (app);
}
