# loadinganim <br>

**A simple terminal loading message** 

    from loadinganim import LoadingAnim
    import time

    #Animation1
    loader = LoadingAnim(message='Please Wait',animType=0)
    loader.start()
    time.sleep(5)
    loader.stop()

    #Animation2
    loader = LoadingAnim(message='Please Wait',animType=1)
    loader.start()
    time.sleep(5)
    loader.stop()

**Install:**
>pip install loadinganim

For pip3:
>pip3 install loadinganim