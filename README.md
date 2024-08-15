> [!NOTE]  
> This repository has been **migrated** to [git.gay](https://git.gay/trinkey/imageboard). The Github version will **no longer be maintained**.

# imageboard
its kinda cool i guess

## how to use
to run the server, first install the required python libraries (`pip install --upgrade django django-ninja` should be all i think). then create the database (`python manage.py migrate`), then run the server (`python manage.py runserver`). you can specify an ip address like this: `python manage.py runserver 0.0.0.0:80`

assuming you can figure out how to run the server, you can submit images by going to `/submit`, and you can approve images and add tags on the `/admin` page. you can configure the valid admin passwords in the `config.py` file

## todo
- add config setting to change max file size and number of concurrent uploads
- allow changing tags after initially adding the image on the admin page
