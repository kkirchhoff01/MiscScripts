" Path to bundles
execute pathogen#infect()

" General settings
set t_Co=256
syntax on
set number
set wildmenu

" Fix this annoying problem
:command WQ wq
:command Wq wq
:command W w
:command Q q

" vividchalk theme
colorscheme vividchalk

" Filetype plugins
filetype plugin on
filetype plugin indent on

" 4-space tabs
set tabstop=4
set shiftwidth=4
set expandtab
set softtabstop=4

" Shortcut for file browser
nnoremap <C-n> :NERDTreeToggle<CR>

" Tab detection
nnoremap <C-t> :tabnext<CR>
inoremap <C-t> <ESC>:tabnext<CR>

filetype detect

" Execute from vim
if &ft=='python'
    nnoremap <F5> :!python %<CR>
    inoremap <F5> <ESC>:!python %<CR>
elseif &ft=='bash' || &ft=='shell' || &ft=='sh'
    nnoremap <F4> :!chmod +x %<CR>
    inoremap <F4> <ESC>:!chmod +x %<CR>
    nnoremap <F5> :!./%<CR>
    inoremap <F5> <ESC>:!./%<CR>
endif

" LaTeX commands
"let g:tex_flavor='pdflatex'
let g:Tex_DefaultTargetFormat='pdf'
" Evince error redirection
let g:Tex_ViewRule_pdf='evince 2>/dev/null'
let g:Tex_ViewRule_pdf='evince>/dev/null'
