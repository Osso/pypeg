let SessionLoad = 1
if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
imap <silent> <Plug>IMAP_JumpBack =IMAP_Jumpfunc('b', 0)
imap <silent> <Plug>IMAP_JumpForward =IMAP_Jumpfunc('', 0)
map! <D-v> *
smap 	 i<BS>	
vmap <NL> <Plug>IMAP_JumpForward
nmap <NL> <Plug>IMAP_JumpForward
nmap o <Plug>ZoomWin
map e :VSBufExplorer
noremap  `"
nmap ,ca <Plug>CVSAdd
nmap ,cd <Plug>CVSDiff
nmap ,cc <Plug>CVSCommit
nmap ,e :BufExplorer
nmap ,t :Tlist
vmap ,b :call VBlockquote()
vmap ,kpq :s/^> *[a-zA-Z]*>/> >/
map ,mlu 1G}OPriority: urgent
map ,cs 1G/^Subject: yypIX-Old--W
nmap ,c <Plug>Traditional
vmap ,c <Plug>VisualTraditional
vmap ,QPE :!qpencode
vmap ,QPD :!qpdecode 
nmap 2HTML :so $VIMRUNTIME/syntax/2html.vim
nnoremap <silent> <<Right> :wincmd l 
nnoremap <silent> <<Left> :wincmd h
nnoremap <silent> <<Down> :wincmd j
nnoremap <silent> <<Up> :wincmd k 
vnoremap < <gv
vnoremap > >gv
imap <silent> Ã¸ <Plug>FirstLine
imap <silent> Ã£ <Plug>FirstLineji
map Q gq
map <silent> \ta :call TableAlign()
map <silent> \th :call TableHeading()
map <silent> \tt :call TableToggle()
nmap \cwr <Plug>CVSWatchRemove
nmap \cwf <Plug>CVSWatchOff
nmap \cwn <Plug>CVSWatchOn
nmap \cwa <Plug>CVSWatchAdd
nmap \cwv <Plug>CVSWatchers
nmap \cv <Plug>CVSVimDiff
nmap \cu <Plug>CVSUpdate
nmap \ct <Plug>CVSUnedit
nmap \cs <Plug>CVSStatus
nmap \cr <Plug>CVSReview
nmap \cq <Plug>CVSRevert
nmap \cl <Plug>CVSLog
nmap \cg <Plug>CVSGotoOriginal
nmap \ci <Plug>CVSEditors
nmap \ce <Plug>CVSEdit
nmap \cG <Plug>CVSClearAndGotoOriginal
nmap \cn <Plug>CVSAnnotate
map \rwp <Plug>RestoreWinPosn
map \swp <Plug>SaveWinPosn
nmap \ch <Plug>CalendarH
nmap \ca <Plug>CalendarV
nmap \s :call InitShell()
vmap dr :!tr A-Za-z N-ZA-Mn-za-m
nmap gx <Plug>NetrwBrowseX
noremap gf gf`"
map <F1> :!python %
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#NetrwBrowseX(expand("<cWORD>"),0)
nmap <F5> :make
vmap <silent> <Plug>IMAP_JumpBack `<i=IMAP_Jumpfunc('b', 0)
vmap <silent> <Plug>IMAP_JumpForward i=IMAP_Jumpfunc('', 0)
vmap <silent> <Plug>IMAP_DeleteAndJumpBack "_<Del>i=IMAP_Jumpfunc('b', 0)
vmap <silent> <Plug>IMAP_DeleteAndJumpForward "_<Del>i=IMAP_Jumpfunc('', 0)
nmap <silent> <Plug>IMAP_JumpBack i=IMAP_Jumpfunc('b', 0)
nmap <silent> <Plug>IMAP_JumpForward i=IMAP_Jumpfunc('', 0)
nnoremap <silent> <Plug>CVSWatchRemove :CVSWatchRemove
nnoremap <silent> <Plug>CVSWatchOff :CVSWatchOff
nnoremap <silent> <Plug>CVSWatchOn :CVSWatchOn
nnoremap <silent> <Plug>CVSWatchAdd :CVSWatchAdd
nnoremap <silent> <Plug>CVSWatchers :CVSWatchers
nnoremap <silent> <Plug>CVSVimDiff :CVSVimDiff
nnoremap <silent> <Plug>CVSUpdate :CVSUpdate
nnoremap <silent> <Plug>CVSUnedit :CVSUnedit
nnoremap <silent> <Plug>CVSStatus :CVSStatus
nnoremap <silent> <Plug>CVSReview :CVSReview
nnoremap <silent> <Plug>CVSRevert :CVSRevert
nnoremap <silent> <Plug>CVSLog :CVSLog
nnoremap <silent> <Plug>CVSClearAndGotoOriginal :CVSGotoOriginal!
nnoremap <silent> <Plug>CVSGotoOriginal :CVSGotoOriginal
nnoremap <silent> <Plug>CVSEditors :CVSEditors
nnoremap <silent> <Plug>CVSEdit :CVSEdit
nnoremap <silent> <Plug>CVSDiff :CVSDiff
nnoremap <silent> <Plug>CVSCommit :CVSCommit
nnoremap <silent> <Plug>CVSAnnotate :CVSAnnotate
nnoremap <silent> <Plug>CVSAdd :CVSAdd
nmap <silent> <Plug>RestoreWinPosn :call RestoreWinPosn()
nmap <silent> <Plug>SaveWinPosn :call SaveWinPosn()
nmap <silent> <Plug>CalendarH :cal Calendar(1)
nmap <silent> <Plug>CalendarV :cal Calendar(0)
noremap <Plug>VisualFirstLine :call EnhancedCommentify('', 'first',				    line("'<"), line("'>"))
noremap <Plug>VisualTraditional :call EnhancedCommentify('', 'guess',				    line("'<"), line("'>"))
noremap <Plug>VisualDeComment :call EnhancedCommentify('', 'decomment',				    line("'<"), line("'>"))
noremap <Plug>VisualComment :call EnhancedCommentify('', 'comment',				    line("'<"), line("'>"))
noremap <Plug>FirstLine :call EnhancedCommentify('', 'first')
noremap <Plug>Traditional :call EnhancedCommentify('', 'guess')
noremap <Plug>DeComment :call EnhancedCommentify('', 'decomment')
noremap <Plug>Comment :call EnhancedCommentify('', 'comment')
map <F7> :WMToggle
map <F8> :set hls!
vmap <BS> "-d
vmap <D-x> "*d
vmap <D-c> "*y
vmap <D-v> "-d"*P
nmap <D-v> "*P
imap 	 <Plug>Jumper
imap <NL> <Plug>IMAP_JumpForward
imap BX_ ,------[]`------[]<Up>| 
vmap <silent> Ã¸ <Plug>VisualFirstLine
vmap <silent> Ã£ <Plug>VisualFirstLinej
nmap <silent> Ã¸ <Plug>FirstLine
nmap <silent> Ã£ <Plug>FirstLinej
vmap üx s,----[]`----Pv`]:s/^/| /'[k$i
map üc :call CommentToggleSmart("0", "#")
abbr Fdeny http://www.iks-jena.de/mitarb/usenet/Firewall.html#Deny
abbr Fnews http://www.cgarbers.de/newsreaderFAQ.php3
abbr Flutz http://www.iks-jena.de/mitarb/lutz/usenet/Firewall.html
abbr Foe http://oe-faq.de.vu
abbr FpgpETH http://computing.ee.ethz.ch/.doc/pgp/index.de.htm
abbr Fapacheml http://www.unix-ag.org/apachelist/
abbr Fdciwsfaq http://www.mela.de/Unix/FAQ/
abbr Fapachedoc http://www.apache.org/docs/
abbr Fshell http://www.koehntopp.de/kris/artikel/unix/shellprogrammierung/
abbr Fsmtpauthpatch http://www.sendmail.org/~ca/email/authrealms.html 
abbr Fsmtpauthhowto http://grisu.x-networks.de/linux/doku/smtpauth-howto.html
abbr Fsmtpauth http://www.sendmail.org/~ca/email/auth.html 
abbr Fsmrewrite http://www.guug.de/~roessler/genericstable.html
abbr Fperlidiotsguide http://www.perl.com/CPAN-local/doc/FAQs/cgi/idiots-guide.html
abbr Fperlcheckliste http://martin.sluka.de/Perl-Checkliste.html
abbr Fdclpmfaq http://www.worldmusic.de/perl/mini-faq.html
abbr Fdclpcfaq http://www.worldmusic.de/perl/dclpc-faq.html
abbr Fsecdebian http://joker.rhwd.de/doc/Securing-Debian-HOWTO
abbr Ftuxpics http://www.home.unix-ag.org/simon/pingu.html
abbr Fhowtode http://www.tu-harburg.de/dlhp/
abbr Fhowto http://www.linuxdoc.org/
abbr Fspamblock http://www.belwue.de/wwwservices/hilfestellungen/spamblock.html
abbr lynxsslpatch http://www.moxienet.com/lynx/
abbr Fqoute http://learn.to/qoute
abbr Fquote http://www.afaik.de/usenet/faq/zitieren/
abbr Fdanamfaq http://home.snafu.de/laura/de.admin.net-abuse.mail.txt
abbr Ffaqfreieserver http://www.qad.org/faq/faq-freie.html
abbr Fmessageid http://www.qad.org/faq/faq-messageid.html
abbr Fusenetunbeliebt http://home.wtal.de/kender/ways.html
abbr Fusenetdeinfos http://www.rewi.hu-berlin.de/~gerlach/dni/index.html
abbr Ffalscheemailad http://www.rewi.hu-berlin.de/~gerlach/falsche-email-adressen.html
abbr Fheaderzeilen http://www.rewi.hu-berlin.de/~gerlach/dni/headerzeilen.html
abbr Fnettiquette http://www-old.uni-bremen.de/zfn/regelungen/nettiquette.html
abbr Fusenetsubject http://www.perl.com/CPAN-local/authors/Dean_Roehrich/subjects.post
abbr Tyoda http://yoda.trash.net/userzone/thomasb
abbr Tmysql http://www.trash.net/dienste/mysql.shtml
abbr Tgpg http://www.linux-magazin.de/ausgabe/1999/12/GnuPG/gnupg.html
abbr Thtaccess http://www.trash.net/faq/htaccess.shtml
abbr Upageeniac http://www.eniac.ch.eu.org/~thomasb/
abbr Ulist http://lists.t-bader.ch/
abbr Upagetrash http://www.trash.net/~thomasb/
abbr Upagetb http://www.t-bader.ch/
abbr Ueniac thomasb@eniac.ch.eu.org
abbr Umailtb thomas@t-bader.ch
abbr Umailtrash thomasb@trash.net
iabbr felt fehlt
iabbr du Du
iabbr DU Du
iabbr sit ist
iabbr Dreckfuhler Druckfehler
iabbr doer oder
iabbr nciht nicht
iabbr tpyo typo
iabbr Srever Server
iabbr teh the
iabbr relyast relayst
iabbr gerarten geraten
iabbr gearten geraten
iabbr seperate separate
iabbr shoudl should
iabbr exmaples examples
iabbr exmaple example
iabbr charcters characters
iabbr charcter character
iabbr bianries binaries
iabbr bianry binary
iabbr aslo also
iabbr alos also
let &cpo=s:cpo_save
unlet s:cpo_save
set autoindent
set autowrite
set background=dark
set backspace=2
set comments=b:#,b:%,b:-,n:>,n:),b:|
set expandtab
set fileencodings=ucs-bom,utf-8,default,latin1
set grepprg=grep\ -nH\ $*
set helplang=de
set hidden
set highlight=8r,db,es,hs,mb,Mr,nu,rs,sr,tb,vr,ws
set ignorecase
set iskeyword=@,48-57,_,192-255,p,f,g,e,t,c,l,a,s,i,d,n,b,1,k,o,r,m
set laststatus=2
set lazyredraw
set listchars=tab:»·,trail:·
set pastetoggle=<F11>
set report=0
set ruler
set shiftwidth=4
set showmatch
set statusline=%1*[%02n]%*\ %(%M%R%H%)\ *\ %2*%t%*\ *%=%{Options()}\ %3*<%l,%c%V,%p%%>%*
set suffixes=.aux,.bak,.dvi,.gz,.idx,.log,.ps,.swp,.tar
set tabstop=4
set wildignore=*.pyc
set wildmode=longest,list
set nowritebackup
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/pyPEG2
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 sample1.py
badd +1 pyPEG2.py
badd +1 test_pyPEG2.py
badd +1 sample2.py
silent! argdel *
edit pyPEG2.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 102 + 102) / 204)
exe 'vert 2resize ' . ((&columns * 101 + 102) / 204)
argglobal
setlocal autoindent
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=b:#,b:%,b:-,n:>,n:),b:|
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
setlocal foldmethod=manual
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=0
setlocal include=s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255,p,f,g,e,t,c,l,a,s,i,d,n,b,1,k,o,r,m
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=octal,hex
setlocal nonumber
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=0
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit test_pyPEG2.py
setlocal autoindent
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=b:#,b:%,b:-,n:>,n:),b:|
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
setlocal foldmethod=manual
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=0
setlocal include=s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255,p,f,g,e,t,c,l,a,s,i,d,n,b,1,k,o,r,m
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=octal,hex
setlocal nonumber
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=0
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 102 + 102) / 204)
exe 'vert 2resize ' . ((&columns * 101 + 102) / 204)
tabedit sample1.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 102 + 102) / 204)
exe 'vert 2resize ' . ((&columns * 101 + 102) / 204)
argglobal
setlocal autoindent
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=b:#,b:%,b:-,n:>,n:),b:|
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
setlocal foldmethod=manual
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=0
setlocal include=s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255,p,f,g,e,t,c,l,a,s,i,d,n,b,1,k,o,r,m
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=octal,hex
setlocal nonumber
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=0
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit sample2.py
setlocal autoindent
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
setlocal comments=b:#,b:%,b:-,n:>,n:),b:|
setlocal commentstring=#%s
setlocal complete=.,w,b,u,t,i
setlocal completefunc=
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal expandtab
if &filetype != 'python'
setlocal filetype=python
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
setlocal foldmethod=manual
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=0
setlocal include=s*\\(from\\|import\\)
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetPythonIndent(v:lnum)
setlocal indentkeys=0{,0},:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
setlocal iskeyword=@,48-57,_,192-255,p,f,g,e,t,c,l,a,s,i,d,n,b,1,k,o,r,m
setlocal keywordprg=
setlocal nolinebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=octal,hex
setlocal nonumber
setlocal numberwidth=4
setlocal omnifunc=pythoncomplete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
setlocal syntax=python
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=0
setlocal thesaurus=
setlocal noundofile
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 102 + 102) / 204)
exe 'vert 2resize ' . ((&columns * 101 + 102) / 204)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
