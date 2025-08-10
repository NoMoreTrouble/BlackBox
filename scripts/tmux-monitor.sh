#!/usr/bin/env bash
tmux new-session -d -s plantmon
tmux rename-window 'app'
tmux send-keys -t plantmon 'tail -f var/log/app.log' C-m
tmux split-window -h
tmux send-keys -t plantmon 'tail -f var/log/control.log' C-m
tmux split-window -v
tmux send-keys -t plantmon 'tail -f var/log/actuators.log' C-m
tmux select-pane -t 0
tmux split-window -v
tmux send-keys -t plantmon 'tail -f var/log/updates.log' C-m
tmux attach -t plantmon
