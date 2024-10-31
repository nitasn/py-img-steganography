from utils import colors
import sys
import tty
import termios


def getch():
  """Reads a single character from standard input."""
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(fd)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  # Handle Ctrl+C (SIGINT)
  if ord(ch) == 3:
    raise KeyboardInterrupt
  # Handle Ctrl+D (EOF)
  elif ord(ch) == 4:
    raise EOFError
  # Handle Backspace
  elif ord(ch) == 127:
    ch = '\b'
  return ch


def input_with_default(prompt, default):
  """Displays a prompt with a default value in gray.
  When the user starts typing, the default disappears."""
  prompt = f"{prompt} "
  
  if not sys.stdin.isatty() or not sys.stdout.isatty():
    # Not connected to a terminal, fall back to standard input
    res = input(f"{prompt}[{default}] ")
    if res == '':
      return default
    else:
      return res
          
  sys.stdout.write(f"{prompt}{colors.gray}{default}{colors.reset}")
  sys.stdout.flush()
  input_chars = []
  default_displayed = True

  try:
    while True:
      ch = getch()

      # If Enter is pressed
      if ch == '\n' or ch == '\r':
        sys.stdout.write(colors.reset)
        break
      # If Backspace is pressed
      elif ch == '\b':
        if input_chars:
          input_chars.pop()
          # Move cursor back, overwrite the character with space, move back again
          sys.stdout.write('\b \b')
          sys.stdout.flush()
        elif default_displayed:
          # Clear the default text
          num_chars = len(default)
          sys.stdout.write('\r')  # Move cursor to the beginning
          sys.stdout.write(' ' * (len(prompt) + num_chars))  # Overwrite with spaces
          sys.stdout.write('\r')  # Move cursor back again
          sys.stdout.write(prompt)  # Reprint prompt
          sys.stdout.flush()
          default_displayed = False
          sys.stdout.write(colors.bold)
          sys.stdout.flush()
      # If this is the first character typed
      elif default_displayed:
        # Clear the default text
        num_chars = len(default)
        sys.stdout.write('\r')  # Move cursor to the beginning
        sys.stdout.write(' ' * (len(prompt) + num_chars))  # Overwrite with spaces
        sys.stdout.write('\r')  # Move cursor back again
        sys.stdout.write(prompt)  # Reprint prompt
        sys.stdout.flush()
        default_displayed = False
        input_chars.append(ch)
        sys.stdout.write(colors.bold)
        sys.stdout.write(ch)
        sys.stdout.flush()
      else:
        input_chars.append(ch)
        sys.stdout.write(ch)
        sys.stdout.flush()
  except (KeyboardInterrupt, EOFError):
    sys.stdout.write('\n')
    sys.stdout.flush()
    raise

  # Move to the next line after input is complete
  print()

  # If no input was given, return the default
  if not input_chars and default_displayed:
    return default
  else:
    return ''.join(input_chars)
