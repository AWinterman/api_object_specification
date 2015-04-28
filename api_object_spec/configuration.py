import logging

max_generation_count = 10

loglevel = logging.WARN

console = logging.StreamHandler()
console.setLevel(loglevel)

logging.basicConfig(
     level=loglevel,
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )

logging.getLogger('').addHandler(console)

