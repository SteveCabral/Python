"""Thanksgiving (PyGame) - mouse-driven fullscreen port.

Features:
- Fullscreen on launch
- Clickable control buttons: Add Player, Start Game, Next Player, Next Phrase, Quit
- Player list on left with increased row spacing
- Timer resets on Next Player and on letter guesses
- Start Game preserves player names and resets scores
- Next Phrase resets played flags
- A-Z keys reserved for guessing only; name entry uses text input
- Phrase display: white boxes for letters (underscore if hidden), green boxes for spaces
"""

import sys
import json
from pathlib import Path
import pygame


BG_COLOR = (0, 0, 0)
FPS = 30


def load_config():
    cfg_path = Path(__file__).parent.parent / 'Thanksgiving' / 'game_config.json'
    if not cfg_path.exists():
        return {'phrases': [], 'points': {}, 'time_limit': 20}
    with cfg_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    data.setdefault('phrases', [])
    data.setdefault('points', {})
    data.setdefault('time_limit', 20)
    return data


class Phrase:
    def __init__(self, phrase, category=''):
        self.phrase = phrase.upper()
        self.category = category
        self.available = True


class PhraseManager:
    def __init__(self, phrases):
        self._phrases = [Phrase(p.get('phrase', ''), p.get('category', '')) for p in phrases]

    def next_available(self):
        for p in self._phrases:
            if p.available:
                return p
        return None

    def mark_unavailable(self, phrase_obj):
        for p in self._phrases:
            if p is phrase_obj:
                p.available = False
                return


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.played = False


class Game:
    def __init__(self, screen, config):
        self.screen = screen
        self.cfg = config
        self.phrase_manager = PhraseManager(self.cfg.get('phrases', []))
        self.points_map = {k.upper(): v for k, v in self.cfg.get('points', {}).items()}
        self.time_limit = int(self.cfg.get('time_limit', 20))

        sw, sh = self.screen.get_size()
        self.left_w = int(sw * 0.28)
        self.screen_w = sw
        self.screen_h = sh

        # control buttons
        self.control_buttons = []
        btn_w = 160
        btn_h = 48
        spacing = 12
        base_x = self.left_w + 24
        base_y = self.screen_h - btn_h - 24
        labels = ['Add Player', 'Start Game', 'Next Player', 'Next Phrase', 'Quit']
        for i, lab in enumerate(labels):
            r = pygame.Rect(base_x + i * (btn_w + spacing), base_y, btn_w, btn_h)
            self.control_buttons.append({'label': lab, 'rect': r})

        self.players = []
        self.current_player_idx = None

        self.current_phrase = None
        self.revealed = set()
        self.timer_active = False
        self.time_remaining = self.time_limit
        self.last_tick = pygame.time.get_ticks()

        self.next_enabled = False
        self.status = 'Click Add Player to begin, Start Game to load a phrase.'

    def add_player(self, name):
        if not name.strip():
            return
        if any(p.name.lower() == name.lower() for p in self.players):
            return
        self.players.append(Player(name.strip()))
        if self.current_player_idx is None:
            self.current_player_idx = 0

    def reset_scores(self):
        for p in self.players:
            p.score = 0
            p.played = False

    def reset_played_flags(self):
        for p in self.players:
            p.played = False

    def start_game(self):
        self.reset_scores()
        self.phrase_manager = PhraseManager(self.cfg.get('phrases', []))
        self.next_phrase()
        self.status = 'Game started.'

    def next_player(self):
        if not self.players:
            return
        if self.current_player_idx is None:
            self.current_player_idx = 0
        else:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self.time_remaining = self.time_limit
        self.timer_active = True

    def next_phrase(self):
        self.reset_played_flags()
        ph = self.phrase_manager.next_available()
        if not ph:
            self.current_phrase = None
            self.status = 'No more phrases.'
            self.timer_active = False
            return
        self.current_phrase = ph
        # reveal non-letters (spaces/punctuation); letters hidden
        self.revealed = set(ch for ch in self.current_phrase.phrase if not ch.isalpha())
        self.time_remaining = self.time_limit
        self.timer_active = False
        self.next_enabled = False
        self.status = f"Loaded phrase ({self.current_phrase.category})"

    def on_letter(self, ch):
        ch = ch.upper()
        if not self.current_phrase:
            return
        if ch in self.revealed:
            return
        self.time_remaining = self.time_limit
        self.timer_active = True
        occ = self.current_phrase.phrase.count(ch)
        if occ > 0:
            self.revealed.update([ch])
            pts = self.points_map.get(ch, 5)
            if self.current_player_idx is not None:
                self.players[self.current_player_idx].score += pts * occ
                self.players[self.current_player_idx].played = True
            self.status = f"{ch} found {occ} time(s). +{pts*occ}"
            # check fully revealed
            all_letters = {c for c in self.current_phrase.phrase if c.isalpha()}
            if all_letters.issubset(self.revealed):
                self.phrase_manager.mark_unavailable(self.current_phrase)
                self.next_enabled = True
                self.timer_active = False
                self.status = 'Phrase solved. Click Next Phrase.'
        else:
            cost = self.points_map.get(ch, 5)
            if self.current_player_idx is not None:
                self.players[self.current_player_idx].score -= cost
                self.players[self.current_player_idx].played = True
            self.status = f"{ch} not in phrase. -{cost}"

    def update_timer(self):
        if not self.timer_active:
            return
        now = pygame.time.get_ticks()
        if now - self.last_tick >= 1000:
            self.time_remaining -= 1
            self.last_tick = now
            if self.time_remaining <= 0:
                self.timer_active = False
                self.status = 'Time up for current player.'

    def draw(self):
        screen = self.screen
        screen.fill(BG_COLOR)

        # left pane - players
        pygame.draw.rect(screen, (18, 18, 18), (0, 0, self.left_w, self.screen_h))
        title_font = pygame.font.SysFont('consolas', 26, bold=True)
        font = pygame.font.SysFont('consolas', 20)
        small = pygame.font.SysFont('consolas', 16)
        title = title_font.render('Leaderboard', True, (200, 200, 200))
        screen.blit(title, (12, 12))
        y = 64
        row_h = 68
        for i, p in enumerate(self.players):
            sel = (i == self.current_player_idx)
            name_s = font.render(f"{i+1}. {p.name}", True, (255, 255, 255))
            score_s = font.render(f"{p.score}", True, (255, 255, 255))
            played_s = small.render('Yes' if p.played else 'No', True, (200, 200, 200))
            screen.blit(name_s, (12, y))
            screen.blit(score_s, (self.left_w - 120, y))
            screen.blit(played_s, (self.left_w - 56, y))
            if sel:
                pygame.draw.rect(screen, (60, 120, 180), (6, y - 8, self.left_w - 12, row_h - 8), 3)
            y += row_h

        # right/main area
        main_x = self.left_w + 24

        # timer and current player
        timer_font = pygame.font.SysFont('consolas', 56)
        tm_col = (220, 30, 30)
        tm_s = timer_font.render(f"{self.time_remaining:02d}", True, tm_col)
        screen.blit(tm_s, (main_x, 8))
        cur_name = 'None'
        if self.current_player_idx is not None and self.players:
            cur_name = self.players[self.current_player_idx].name
        cur_s = pygame.font.SysFont('consolas', 24).render(f"Current: {cur_name}", True, (255, 255, 255))
        screen.blit(cur_s, (main_x + 160, 26))

        # phrase grid with colored placeholders
        phrase_box_y = 120
        phrase_font = pygame.font.SysFont('consolas', 30)
        box_w = 56
        box_h = 64
        gap = 8
        max_row_width = self.screen_w - main_x - 40
        x = main_x
        y = phrase_box_y
        if self.current_phrase:
            for ch in self.current_phrase.phrase:
                if x + box_w > main_x + max_row_width:
                    x = main_x
                    y += box_h + gap

                if ch == ' ':
                    bg = (0, 160, 80)  # green
                    text = ''
                    txt_col = (0, 0, 0)
                elif ch.isalpha():
                    bg = (255, 255, 255)  # white for letter placeholders
                    if ch in self.revealed:
                        text = ch
                    else:
                        text = '_'
                    txt_col = (0, 0, 0)
                else:
                    bg = (255, 255, 255)
                    text = ch
                    txt_col = (0, 0, 0)

                rect = pygame.Rect(x, y, box_w, box_h)
                pygame.draw.rect(screen, bg, rect)
                pygame.draw.rect(screen, (100, 100, 100), rect, 2)
                if text:
                    txt_s = phrase_font.render(text, True, txt_col)
                    tx = rect.x + (rect.width - txt_s.get_width()) // 2
                    ty = rect.y + (rect.height - txt_s.get_height()) // 2
                    screen.blit(txt_s, (tx, ty))

                x += box_w + gap
        else:
            no_s = phrase_font.render('No phrase loaded', True, (200, 200, 200))
            screen.blit(no_s, (main_x, phrase_box_y))

        # category and status
        cat_s = pygame.font.SysFont('consolas', 18).render(f"Category: {self.current_phrase.category if self.current_phrase else ''}", True, (220, 220, 220))
        screen.blit(cat_s, (main_x, phrase_box_y + 220))
        status_s = pygame.font.SysFont('consolas', 16).render(self.status, True, (220, 220, 220))
        screen.blit(status_s, (main_x, phrase_box_y + 250))

        # control buttons
        for b in self.control_buttons:
            pygame.draw.rect(screen, (100, 140, 200), b['rect'], border_radius=6)
            lab_s = pygame.font.SysFont('consolas', 18).render(b['label'], True, (255, 255, 255))
            lx = b['rect'].x + (b['rect'].width - lab_s.get_width()) // 2
            ly = b['rect'].y + (b['rect'].height - lab_s.get_height()) // 2
            screen.blit(lab_s, (lx, ly))

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Thanksgiving - PyGame Version')
    clock = pygame.time.Clock()

    cfg = load_config()
    game = Game(screen, cfg)

    adding_name = False
    name_buf = ''

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if adding_name:
                    if event.key == pygame.K_ESCAPE:
                        adding_name = False
                        name_buf = ''
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        game.add_player(name_buf)
                        adding_name = False
                        name_buf = ''
                    elif event.key == pygame.K_BACKSPACE:
                        name_buf = name_buf[:-1]
                    else:
                        ch = event.unicode
                        if ch and ch.isprintable():
                            name_buf += ch
                else:
                    # Only treat A-Z as guesses; ignore other keyboard commands
                    if event.unicode and event.unicode.isalpha():
                        game.on_letter(event.unicode.upper())

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for b in game.control_buttons:
                    if b['rect'].collidepoint(mx, my):
                        lab = b['label']
                        if lab == 'Add Player':
                            adding_name = True
                            name_buf = ''
                        elif lab == 'Start Game':
                            game.start_game()
                        elif lab == 'Next Player':
                            game.next_player()
                        elif lab == 'Next Phrase':
                            game.next_phrase()
                        elif lab == 'Quit':
                            running = False
                        break

        game.update_timer()
        game.draw()

        # overlay input when adding a player
        if adding_name:
            sw, sh = screen.get_size()
            overlay = pygame.Surface((sw, 80))
            overlay.set_alpha(230)
            overlay.fill((255, 255, 255))
            screen.blit(overlay, (0, sh // 2 - 40))
            prompt = pygame.font.SysFont('consolas', 22).render('Enter player name: ' + name_buf, True, (0, 0, 0))
            lx = game.left_w + 20 if hasattr(game, 'left_w') else 20
            screen.blit(prompt, (lx, sh // 2 - 20))
            pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()