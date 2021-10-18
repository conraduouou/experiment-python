from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image


# constants
WIDTH = 800
HEIGHT = 500

# to make space for other buttons to be placed in the bottom of the window
height_gap = 100

# for upscaling to work properly, and not make small pictures have maxed widths all the time
width_gap = 300


# confirm quit process
def confirm_quit(*args):
    if messagebox.askyesno('Confirm Exit', 'Do you wish to quit?'):
        exit()


# make the start widgets specified 'invisible', making for smooth transitions
def forget_start():
    start_button.place_forget()
    start_label.place_forget()


# make the watermark widgets specified 'invisible', making for smooth transitions
def forget_wmark():
    wmark_button.place_forget()


# resize file however large or small to scale towards window size
def scale_photo(photo):
    if photo.width < WIDTH - width_gap and photo.height < (HEIGHT - height_gap):
        photo = photo.resize(
            (
                WIDTH - width_gap,
                int(photo.height * (1 + (((WIDTH - width_gap) - photo.width) / photo.width)))
            )
        )
    else:
        if photo.width > WIDTH:
            photo = photo.resize(
                (
                    photo.width - (photo.width - WIDTH), 
                    int(photo.height * (1 - ((photo.width - WIDTH) / photo.width)))
                )
            )
        elif photo.height > (HEIGHT - height_gap):
            photo = photo.resize(
                (
                    int(photo.width * (1 - ((photo.height - (HEIGHT - height_gap)) / photo.height))), 
                    photo.height - (photo.height - (HEIGHT - height_gap))
                )
            )
        else:
            return photo

    return scale_photo(photo)


# resize watermark image to fit picture
def scale_watermark(photo, watermark):
    if watermark.width < photo.width / 6 and watermark.height < photo.height / 7:
        watermark = watermark.resize(
            (
                int(photo.width / 5),
                int(photo.height * (1 + (((photo.width / 5) - photo.width) / watermark.width)))
            )
        )
    else:
        if watermark.width > photo.width / 5:
            watermark = watermark.resize(
                (
                    int(photo.width / 5), 
                    int(watermark.height * (1 - ((watermark.width - (photo.width / 5)) / watermark.width)))
                )
            )
        elif watermark.height > photo.height / 6:
            watermark = watermark.resize(
                (
                    int(watermark.width * (1 - ((watermark.height - (photo.height / 6)) / watermark.height))), 
                    int(photo.height / 6)
                )
            )
        else:
            return watermark

    return scale_watermark(photo, watermark)



# file explorer to import images
def browse_files() -> str:
    filename = filedialog.askopenfilename(
        initialdir = "DAY 84 - WatermarkER/",
        title = "Select a File",
        filetypes = (
            ("PNG files", "*.png"),
            ("all files", "*.*"),
            ("JPEG/JPG files", '*.jp*g')    
        )
    )

    return filename


# show image to watermark
def show_image():
    filename = browse_files()

    forget_start()

    # open file using PIL Image class first before giving Tk integration
    orig_image.image = Image.open(filename)

    scaled_photo = scale_photo(orig_image.image)

    # scale the copy of the photo down/up by resizing and then make it viewable in Tk window
    # this is to ensure that the dimensions of the original file is not changed, and that the watermark
    # is applied to to it proportionate to what will be made to the copy.
    photo_file = ImageTk.PhotoImage(scaled_photo)

    image_label.config(image=photo_file)
    image_label.image = photo_file

    image_label.place(x=WIDTH/2 - photo_file.width()/2, y=20)

    image_button.place(x=WIDTH/2 - 180, y=(HEIGHT - height_gap) + 50)
    wmark_button.place(x=WIDTH/2 + 20, y=(HEIGHT - height_gap) + 50)
    save_button.place_forget()


# the function to end everything
def watermark():
    filename = browse_files()

    # open image file to use as watermark
    wmark_image = Image.open(filename)

    wmark_image.paste

    # scale watermark according to original image
    scaled_wmark = scale_watermark(orig_image.image, wmark_image)

    ## use scaled watermark and paste it in the bottom right region of the original image,
    ## store it on wmarked_image label, scale it down,
    ## and then display it on window

    coordinates = {
        'left': int(orig_image.image.width * 23/24 - scaled_wmark.width),
        'upper': int(orig_image.image.height * 27/28 - scaled_wmark.height),
        'right': int(orig_image.image.width * 23/24),
        'lower': int(orig_image.image.height * 27/28)
    }

    wmarked_image.image = orig_image.image
    
    wmarked_image.image.paste(
        scaled_wmark,
        (coordinates['left'], coordinates['upper'], coordinates['right'], coordinates['lower'])
    )

    scaled_output = scale_photo(wmarked_image.image)

    photo_file = ImageTk.PhotoImage(scaled_output)

    image_label.config(image=photo_file)
    image_label.image = photo_file

    image_label.place(x=WIDTH/2 - photo_file.width()/2, y=20)
    
    ## save button place
    save_button.place(x=WIDTH - 120, y=(HEIGHT - height_gap) + 50)
    

# save function
def save_image():
    if messagebox.askyesno('Save Image', 'Do you wish to save current image?'):
        filename = wmarked_image.image.filename.split('/')

        filename[-1] = "wmarked " + filename[-1]

        wmarked_image.image.save('/'.join(filename), wmarked_image.image.format)

        messagebox.showinfo('Successful', 'Successfully saved image.')




# construct window
window = Tk()
window.title('WatermarkER')     # this can't be configured in the config, or I just can't
window.resizable(width=False, height=False)
window.minsize(width=WIDTH, height=HEIGHT)

# make exit key
window.bind('<Escape>', confirm_quit)

is_watermarked = False


## -- START CONTENT -- 
# exit instruction
start_label = Label(text='Press ESC to exit')
start_label.place(x=360, y=0)

# start button to initiate edit process
start_button = Button(text='Start Watermarking', command=show_image)
start_button.place(x=350, y=220)


## -- WATERMARK CONTENT -- 
image_button = Button(text='Choose another image...', command=show_image)
wmark_button = Button(text='Choose image as watermark..', command=watermark)
save_button = Button(text='Save', command=save_image)


## -- IMAGE file --
orig_image = Label()        # placeholder for original image file
wmarked_image = Label()     # placeholder for watermarked image
image_label = Label()       # label that shows scaled image


# not quitting until specified by program or close button is pressed
window.mainloop()