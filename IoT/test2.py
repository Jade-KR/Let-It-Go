with open("ba-1.raw", "rb") as f:
  with open("ba-1-1.raw", "wb") as f2:
    f2.write(f.read())
