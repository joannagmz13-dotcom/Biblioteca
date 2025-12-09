from django.urls import path

from . import views

urlpatterns = [

    path('logout/', views.logout_view, name='logout'),  # ⬅ importante
    path('lista-alumno/', views.alumno_list, name='alumno_list'),
    path('alumno/nuevo/', views.alumno_create, name='alumno_create'),
    path('editar/<int:id>/', views.alumno_update, name='alumno_update'),
    path('eliminar/<int:id>/', views.alumno_delete, name='alumno_delete'),
    # categorias
    path('lista-categorias/', views.categoria_list, name='categoria_list'),
    path('categoria-nueva/', views.categoria_create, name='categoria_create'),
    path('categoria-editar/<int:id>/', views.categoria_update, name='categoria_update'),
    path('categoria-eliminar/<int:id>/', views.categoria_delete, name='categoria_delete'),

    path('lista-autores/', views.autor_list, name='autor_list'),
    path('autor-nuevo/', views.autor_create, name='autor_create'),
    path('autor-editar/<int:id>/', views.autor_update, name='autor_update'),
    path('autor-eliminar/<int:id>/', views.autor_delete, name='autor_delete'),

    path("lista-libros/", views.libro_list, name="libro_list"),
    path("nuevo-libro/", views.libro_create, name="libro_create"),
    path("editar-libro/<int:id>/", views.libro_update, name="libro_update"),
    path("eliminar-libro/<int:id>/", views.libro_delete, name="libro_delete"),

    path('prestamos/nuevo/', views.prestamo_create, name='prestamo_create'),
    path('ejemplares-disponibles/<int:libro_id>/', views.ejemplares_disponibles, name='ejemplares_disponibles'),

    path('prestamos/', views.prestamo_list, name='prestamo_list'),

    # multas

    path("prestamos/devolver/<int:id>/", views.prestamo_devolver, name="prestamo_devolver"),
    path("prestamos/multa/manual/<int:id>/", views.multa_manual, name="multa_manual"),
    path("prestamos/multa/automatica/<int:id>/", views.multa_automatica, name="multa_automatica"),

    path("prestamos/<int:id>/multas/", views.prestamo_multas, name="prestamo_multas"),

    path("prestamos/devolver-sin-multa/<int:id>/", views.prestamo_devolver_sin_multa, name="prestamo_devolver_sin_multa"),

    path("prestamos/multas/<int:id_prestamo>/", views.ver_multas_prestamo),

    path("login/alumno/", views.login_alumno, name="login_alumno"),
    path("alumno/dashboard/", views.alumno_dashboard, name="alumno_dashboard"),
    path("alumno/logout/", views.logout_alumno, name="logout_alumno"),

    path("catalogo/", views.catalogo_libros, name="catalogo_libros"),
    path("catalogo/<int:id>/", views.detalle_libro, name="detalle_libro"),

]
