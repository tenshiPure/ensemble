augroup ensemble
	autocmd!
	autocmd BufEnter *.py set noexpandtab | set tabstop=4 | set shiftwidth=4
	autocmd BufEnter *.html set expandtab | set tabstop=2 | set shiftwidth=2
	autocmd BufEnter *.js   set expandtab | set tabstop=2 | set shiftwidth=2
	autocmd BufEnter *.css  set expandtab | set tabstop=2 | set shiftwidth=2
augroup END
