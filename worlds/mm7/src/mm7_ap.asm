; MM7 Archipelago Patch
; Mega Man 7 (USA)

hirom

; ============================================
; AP WRAM layout
; Using $7E1FA1-$7E1FDF.
; $7E1FA0 appears to be cleared during state transitions.
; ============================================

!AP_BOSS_FLAGS      = $7E1FA1
!AP_BOSS_FLAGS_2    = $7E1FA2
!AP_DEBUG_FLAGS     = $7E1FA3
!AP_ITEM_ID_LO      = $7E1FA4
!AP_ITEM_ID_HI      = $7E1FA5
!AP_EXECUTE_FLAG    = $7E1FA6
!AP_RECV_INDEX_LO   = $7E1FA7
!AP_RECV_INDEX_HI   = $7E1FA8
!AP_CONNECTION      = $7E1FA9
!AP_RUNTIME_START   = $7E1FA1
!MM7_PROTO_FLAGS    = $7E0B78

!AP_PROTO_CHECKS    = $7E1FA2 ; already AP_BOSS_FLAGS_2
!AP_PROTO_ITEMS     = $7E1FAA ; AP-owned randomized Proto clues
!AP_TEMP            = $7E1FAB
!AP_GOAL_FLAGS      = $7E1FAC
!AP_PICKUP_FLAGS    = $7E1FB0 ; legacy alias for Rush flags
!AP_RUSH_FLAGS      = $7E1FB0
!AP_ITEM_FLAGS      = $7E1FB1
!AP_MEGA_FLAGS      = $7E1FB2 ; AP checked flags for $0BB1 mega items
!AP_MISC_FLAGS      = $7E1FB3
!AP_WILY_FLAGS      = $7E1FB4
!AP_WILY_ACCESS     = $7E1FB5
!AP_SELECTED_WILY_STAGE = $7E1FB6
!AP_DRAW_WILY_NUMBER = $7E1FB7

org $C0356D
    NOP
    NOP

; Wily stage-select graphics package hook.
; Original at C03376:
;   LDY #$0C
;   JSR $16D4
; The following JSR $0114 at C0337B is preserved.
org $C03376
    LDY #$0C

org $C034FA
    JSL AP_StageSelectWilyCycleHook
    NOP
    NOP
    NOP
    NOP

org $C03DF6
    JSL AP_PostOAMDrawHook
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; New-game setup
; ============================================

org $C00C22
    LDA #$01
    STA $0B79 ; ???
    STA $0B7A ; Robot Museum Flag
    STA $0B7B ; New stages introduction flag
    STZ $0B7C ; Wily Stage
    JSL AP_SetStartingTanks
    JSL AP_SetStartingItems
    LDA #$82
    STA $0B77
    JSL AP_SetStartingBolts
    JSL AP_ClearRuntime
    NOP
    NOP
    NOP

; ============================================
; Remove Rush Coil as a starting item
; ============================================

org $C00BFC
    LDA #$00 ; Rush Coil Ammo

org $C00C18
    LDA #$00 ; Rush Coil Ammo

; org $C00C54
;     JSR AP_SkipIntroStage
;     BRA $C00C81

; ============================================
; Main loop AP hook
; Replaces:
;   C000AF: JSR $315A
;   C000B2: INC $00D1
; ============================================

org $C000AF
    JSL AP_MainLoopHook
    NOP
    NOP

; ============================================
; Vanilla boss weapon grant left restored but bypassed.
; Boss rewards are AP-only via AP_StageExitAPOnlyBossGate.
; ============================================

org $C00DCB
    LDA #$80
    STA $0B83,X

; ============================================
; Stage select medal hook
; Original:
;   C038CC BD 83 0B    LDA $0B83,X
;   C038CF 10 05       BPL $C038D6
;   C038D1 DA          PHX
;   C038D2 20 02 39    JSR $3902
;   C038D5 FA          PLX
; ============================================

org $C038CC
    JSL AP_StageSelectMedalHook
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Boss spawn defeated-state hook
; ============================================

org $C3035F
    JSL AP_LoadBossDefeatedState

; ============================================
; Proto Man meetings hook
; ============================================

org $C2C4B3
    JML AP_ProtoCloudMeetingGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $C2C4C8
    JML AP_ProtoTurboMeetingGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $C2C4D9
    JML AP_ProtoShieldEncounterGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $C3722E
    JML AP_ProtoShieldRewardCheck
    NOP

; ============================================
; AP-only boss reward gate.
; Always records the AP boss flag and skips vanilla weapon-get.
; ============================================

org $C00DBC
    JML AP_StageExitAPOnlyBossGate
    NOP

; Wily unlock gate.
; Replaces vanilla all-weapons check with AP Wily Access Code checks.

org $C00DE1
    JML AP_WilyUnlockGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Wily Capsule defeated goal hook
; Original:
;   D8DAB4 EE CA 0B    INC $0BCA
;   D8DAB7 A9 08       LDA #$08
; ============================================

org $D8DAB4
    JSL AP_WilyCapsuleDefeatedHook
    NOP

; ============================================
; Rush Search spawn/check AP location hook
; Original:
;   D8D11F AD 97 0B    LDA $0B97
;   D8D122 10 03       BPL $D8D127
;   D8D124 4C DF D1    JMP $D1DF
;   D8D127 60          RTS
; ============================================

org $D8D11F
    JML AP_RushSearchSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Rush Search pickup AP location hook
; Original:
;   D8D128 A9 9C       LDA #$9C
;   D8D12A 8D 97 0B    STA $0B97
;   D8D12D 4C E7 D1    JMP $D1E7
; ============================================

org $D8D128
    JML AP_RushSearchPickupCheck
    NOP
    NOP
    NOP
    NOP

org $D8D9C7
    JML AP_ShopRushSearchCheck
    NOP

org $D8D95F
    JML AP_ShopRushSearchPurchase
    NOP
    NOP

; ============================================
; Rush plate pickup AP location hooks
; Original plate grant handlers are 11 bytes each:
;   LDA #$xx
;   TSB $0BA4
;   JSR $D1D0
;   JMP $D1E7
; ============================================

org $D8D0D2
    JML AP_RushRPlatePickupCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0E8
    JML AP_RushUPlatePickupCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0FE
    JML AP_RushSPlatePickupCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D114
    JML AP_RushHPlatePickupCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Rush plate spawn/check AP location hooks
; ============================================

org $D8D0C7
    JML AP_RushRPlateSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0DD
    JML AP_RushUPlateSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0F3
    JML AP_RushSPlateSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D109
    JML AP_RushHPlateSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Rush Jet spawn/check AP location hook
; Original:
;   D8D130 AD 99 0B    LDA $0B99
;   D8D133 10 03       BPL $D8D138
;   D8D135 4C DF D1    JMP $D1DF
;   D8D138 60          RTS
; ============================================

org $D8D130
    JML AP_RushJetSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Rush Jet pickup AP location hook
; Original:
;   D8D139 A9 9C       LDA #$9C
;   D8D13B 8D 99 0B    STA $0B99
;   D8D13E 4C E7 D1    JMP $D1E7
; ============================================

org $D8D139
    JML AP_RushJetPickupCheck
    NOP
    NOP
    NOP
    NOP

org $D8D9C0
    JML AP_ShopRushJetCheck
    NOP

org $D8D959
    JML AP_ShopRushJetPurchase
    NOP
    NOP

; ============================================
; Freeze Man presence gate.
; Original block:
;   C286ED AD 73 0B    LDA $0B73
;   C286F0 C9 09       CMP #$09
;   C286F2 B0 08       BCS $C286FC
;   C286F4 0A          ASL
;   C286F5 AA          TAX
;   C286F6 BD 83 0B    LDA $0B83,X
;   C286F9 10 01       BPL $C286FC
;   C286FB 60          RTS
; ============================================

org $C286ED
    JML AP_FreezeManPresenceGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $C35117
    JML AP_BeatEncounterGate
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8CE8D
    JML AP_BeatRewardCheck
    NOP

; ============================================
; Exit Unit spawn/check AP location hook
; $0BA4 bit $20 -> AP_ITEM_FLAGS bit $20
; ============================================

org $D8D063
    JML AP_ExitUnitSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D06E
    JML AP_ExitUnitPickupCheck
    NOP
    NOP
    NOP
    NOP

org $D8D995
    JML AP_ShopExitUnitCheck
    NOP
    NOP
    NOP

org $D8D93F
    JML AP_ShopExitUnitPurchase
    NOP
    NOP

org $C14D8D
    JML AP_ExitUnitRushSearchGate
    NOP
    NOP
    NOP
    NOP
    NOP

org $C047EB
    JML AP_ExitUnitMedalCheck
    NOP

; ============================================
; Energy Balancer spawn/check AP location hook
; $0BA4 bit $80 -> AP_ITEM_FLAGS bit $80
; ============================================

org $D8D076
    JML AP_EnergyBalancerSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D081
    JML AP_EnergyBalancerPickupCheck
    NOP
    NOP
    NOP
    NOP

org $D8D9A8
    JML AP_ShopEnergyBalancerCheck
    NOP
    NOP
    NOP

org $D8D949
    JML AP_ShopEnergyBalancerPurchase
    NOP
    NOP

org $C14DAA
    JML AP_EnergyBalancerRushSearchGate
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Hyper Bolt spawn/check AP location hook
; $0BA4 bit $10 -> AP_ITEM_FLAGS bit $10
; ============================================

org $D8D0A1
    JML AP_HyperBoltSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0AC
    JML AP_HyperBoltPickupCheck
    NOP
    NOP
    NOP
    NOP

; ============================================
; Hyper Rocket Buster spawn/check AP location hook
; $0BA4 bit $40 -> AP_ITEM_FLAGS bit $40
; ============================================

org $D8D0B4
    JML AP_HyperRocketBusterSpawnCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D0BF
    JML AP_HyperRocketBusterPickupCheck
    NOP
    NOP
    NOP
    NOP

org $C14D98
    JML AP_HyperRocketBusterRushSearchGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D790
    JML AP_ShopHyperRocketBusterSuperAdapterGate
    NOP
    NOP
    NOP
    NOP
    NOP

org $D8D9B7
    JML AP_ShopHyperRocketBusterCheck
    NOP
    NOP
    NOP

org $D8D953
    JML AP_ShopHyperRocketBusterPurchase
    NOP
    NOP

org $C14D72
    JML AP_MegaItemRushSearchCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $C00DA8
    JML AP_IntroStageClearCheck
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $C00C59
    JML AP_RobotMuseumRouteGate
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

org $C00DD7
    JML AP_RobotMuseumClearCheck
    NOP

; Stage select confirm hook.
; Handles both normal stage confirms and Wily-box confirms.
; Blocks Wily confirm if no AP Wily stage is available.
org $C03504
    JML AP_StageSelectConfirmHook
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

; ============================================
; Small C0-bank helper routines
;
; These stay in bank C0 because they call vanilla RTS routines using JSR.
; Do not move them to bank D8 without adding wrappers.
; ============================================

org $C07C00

AP_MainLoopHook:
    JSR $315A
    INC $00D1
    JSL AP_CheckItemReceive
    RTL

org $C07EC0

AP_StageSelectMedalHook:
    PHP
    SEP #$30
    PHX

    ; X is one of $10,$0E,$0C,$0A,$08,$06,$04,$02.
    ; Convert weapon offset into table index: X / 2.
    TXA
    LSR
    TAX

    LDA.l AP_StageSelectBitMaskTable,x
    AND.l !AP_BOSS_FLAGS
    BEQ .not_cleared

.cleared:
    PLX
    PLP

    ; Original cleared behavior:
    ; PHX
    ; JSR $3902
    ; PLX
    PHX
    JSR $3902
    PLX
    RTL

.not_cleared:
    PLX
    PLP
    RTL

AP_StageSelectWilyCycleHook:
    PHP
    SEP #$30

    ; Preserve replaced vanilla behavior.
    JSR $381C

    ; Only handle/display overlay if cursor is on the Wily box.
    JSR $380E
    BNE .not_wily_box

    ; Cursor is on Wily box. Request post-OAM draw.
    LDA #$01
    STA.l !AP_DRAW_WILY_NUMBER

    ; $00A5 = one-frame input for R/L/X/A
    ; R = $10, L = $20
    LDA $00A5
    AND #$10
    BNE .cycle_forward

    LDA $00A5
    AND #$20
    BNE .cycle_backward

    BRA .finish_vanilla_input

.not_wily_box:
    ; Do not draw the Wily stage number on normal bosses.
    LDA #$00
    STA.l !AP_DRAW_WILY_NUMBER
    BRA .finish_vanilla_input

.cycle_forward:
    JSL AP_SelectNextAvailableWilyStage

    ; Play cursor/change sound if a Wily stage is selected.
    LDA.l !AP_SELECTED_WILY_STAGE
    BEQ .finish_vanilla_input

    LDA #$40
    JSL $C03205

    BRA .finish_vanilla_input

.cycle_backward:
    JSL AP_SelectPreviousAvailableWilyStage

    ; Play cursor/change sound if a Wily stage is selected.
    LDA.l !AP_SELECTED_WILY_STAGE
    BEQ .finish_vanilla_input

    LDA #$40
    JSL $C03205

    BRA .finish_vanilla_input

.finish_vanilla_input:
    PLP

    ; Preserve replaced vanilla behavior and flags for BEQ $C03521.
    LDA $00A6
    AND #$50
    RTL

AP_StageSelectConfirmHook:
    PHP
    SEP #$30

    ; Vanilla confirm path first checks whether the selected icon is Wily.
    ; If this returns nonzero, A already contains the normal stage id.
    JSR $380E
    BNE .normal_stage

    ; Wily box selected. If no AP Wily stage is available, cancel confirm.
    JSL AP_HasAnyAvailableWilyStage
    BCC .cancel_wily_confirm

    ; A valid AP Wily stage exists. Return its stage id in A and continue
    ; at vanilla STA $0B73.
    JSL AP_GetSelectedWilyStageId
    PLP
    JML $C0350F

.normal_stage:
    ; Preserve vanilla behavior: store the normal stage id returned by $380E.
    PLP
    JML $C0350F

.cancel_wily_confirm:
    ; Skip the confirm action entirely.
    PLP
    JML $C03521

AP_PostOAMDrawHook:
    PHP
    SEP #$30

    ; Preserve replaced vanilla behavior.
    LDA #$30
    STA $08FF

    LDA #$E0
    STA $08FD

    ; Only draw if stage-select input hook requested it this frame.
    LDA.l !AP_DRAW_WILY_NUMBER
    BEQ .done

    LDA #$00
    STA.l !AP_DRAW_WILY_NUMBER

    ; Draw after vanilla OAM render/cleanup.
    JSL AP_DrawSelectedWilyStageNumber

.done:
    PLP
    RTL

assert pc() <= $C08000

org $C00DF8
    JML AP_WilyStageClearCheck
    NOP
    NOP
    NOP

; ============================================
; AP custom routines block
;
; Confirmed free space:
;   file offset 0x18EF15
;   CPU address $D8EF15
;   size 0xFEB
;   fill $FF
;
; Keep all general AP routines in this block.
; ============================================

org $D8EF15

AP_SetStartingTanks:
    LDA #$01
    STA $0BA0
    LDA #$00
    STA $0BA1
    LDA #$00
    STA $0BA2
    RTL

AP_SetStartingItems:
    LDA #$00
    STA $0BA4
    RTL

AP_SetStartingBolts:
    LDA #$01
    STA $0BA6
    LDA #$00
    STA $0BA7
    RTL

AP_ClearRuntime:
    PHP
    SEP #$30
    PHX

    LDX #$00
    LDA #$00

.clear_loop:
    STA.l !AP_RUNTIME_START,x
    INX
    CPX #$20
    BNE .clear_loop

    PLX
    PLP
    RTL

AP_SkipIntroStage:
    LDA #$01
    STA $0B73
    RTS

; ============================================
; AP item receive dispatcher
;
; !AP_ITEM_ID_LO     = item id low byte
; !AP_ITEM_ID_HI     = item id high byte
; !AP_EXECUTE_FLAG   = 1 when an item is waiting
; !AP_RECV_INDEX_LO  = received index low byte
; !AP_RECV_INDEX_HI  = received index high byte
; ============================================

AP_CheckItemReceive:
    PHP
    SEP #$30
    PHX

    LDA.l !AP_EXECUTE_FLAG
    BNE +
    JMP .done
+

    ; For now only support IDs $0001-$00FF.
    ; If high byte is nonzero, consume safely.
    LDA.l !AP_ITEM_ID_HI
    BEQ +
    JMP .finish
+

    LDA.l !AP_ITEM_ID_LO

    ; $01-$0B = weapon/Rush table
    CMP #$01
    BCS +
    JMP .finish
+

    CMP #$0C
    BCS +
    JMP .give_weapon_table
+

    ; $0C-$13 = unique item bitfield at $0BA4
    CMP #$14
    BCS +
    JMP .give_unique_bitfield
+

    ; $14 = Proto Shield
    CMP #$14
    BNE +
    JMP .give_proto_shield
+

    ; $15 = Beat
    CMP #$15
    BNE +
    JMP .give_beat
+

    ; $16 = 1-Up
    CMP #$16
    BNE +
    JMP .give_one_up

+

    ; $19 = E-Tank
    CMP #$19
    BNE +
    JMP .give_e_tank
+

    ; $1A = W-Tank
    CMP #$1A
    BNE +
    JMP .give_w_tank
+

    ; $1B = S-Tank
    CMP #$1B
    BNE +
    JMP .give_s_tank
+

    ; $1D = Proto Man Cloud Man clue
    CMP #$1D
    BNE +
    JMP .give_proto_cloud_clue
+

    ; $1E = Proto Man Turbo Man clue
    CMP #$1E
    BNE +
    JMP .give_proto_turbo_clue
+

    ; $1F = Wily 1 Access Code
    CMP #$1F
    BNE +
    JMP .give_wily_1_access
+

    ; $20 = Wily 2 Access Code
    CMP #$20
    BNE +
    JMP .give_wily_2_access
+

    ; $21 = Wily 3 Access Code
    CMP #$21
    BNE +
    JMP .give_wily_3_access
+

    JMP .finish

.give_weapon_table:
    SEC
    SBC #$01
    ASL
    TAX

    ; Save direct-page scratch pointer $00/$01 before using it.
    REP #$20
    LDA $00
    PHA

    LDA.l AP_WeaponAddressTable,x
    STA $00

    SEP #$20
    LDA #$9C
    STA ($00)

    REP #$20
    PLA
    STA $00
    SEP #$20

    JMP .finish

.give_unique_bitfield:
    ; item_id - $0C gives bit index 0-7
    SEC
    SBC #$0C
    TAX

    LDA.l AP_BitMaskTable,x
    ORA.l $7E0BA4
    STA.l $7E0BA4

    ; If all four plates are owned, grant Super Adapter.
    LDA.l $7E0BA4
    AND #$0F
    CMP #$0F
    BEQ .grant_super_adapter

    JMP .finish

.grant_super_adapter:
    LDA #$9C
    STA.l $7E0B9F

    JMP .finish

.give_proto_shield:
    LDA #$9C
    STA.l $7E0B95
    JMP .finish

.give_beat:
    LDA #$84
    STA.l $7E0BA3
    JMP .finish

.give_one_up:
    INC $0B81
    JMP .finish

.give_e_tank:
    INC $0BA0
    JMP .finish

.give_w_tank:
    INC $0BA1
    JMP .finish

.give_s_tank:
    INC $0BA2
    JMP .finish

.give_proto_cloud_clue:
    ; AP owns Proto clue bit 0.
    LDA.l !AP_PROTO_ITEMS
    ORA #$01
    STA.l !AP_PROTO_ITEMS

    ; Also set the vanilla clue bit so the game can use it.
    LDA.l !MM7_PROTO_FLAGS
    ORA #$01
    STA.l !MM7_PROTO_FLAGS

    JMP .finish

.give_proto_turbo_clue:
    ; AP owns Proto clue bit 1.
    LDA.l !AP_PROTO_ITEMS
    ORA #$02
    STA.l !AP_PROTO_ITEMS

    ; Also set the vanilla clue bit so the game can use it.
    LDA.l !MM7_PROTO_FLAGS
    ORA #$02
    STA.l !MM7_PROTO_FLAGS

    JMP .finish

.give_wily_1_access:
    LDA.l !AP_WILY_ACCESS
    ORA #$01
    STA.l !AP_WILY_ACCESS
    JSR AP_EnsureVanillaWilyAvailable
    JMP .finish

.give_wily_2_access:
    LDA.l !AP_WILY_ACCESS
    ORA #$02
    STA.l !AP_WILY_ACCESS
    JSR AP_EnsureVanillaWilyAvailable
    JMP .finish

.give_wily_3_access:
    LDA.l !AP_WILY_ACCESS
    ORA #$04
    STA.l !AP_WILY_ACCESS
    JSR AP_EnsureVanillaWilyAvailable
    JMP .finish

.finish:
    ; Increment 16-bit received index stored as two bytes.
    LDA.l !AP_RECV_INDEX_LO
    INC
    STA.l !AP_RECV_INDEX_LO
    BNE .clear_flag

    LDA.l !AP_RECV_INDEX_HI
    INC
    STA.l !AP_RECV_INDEX_HI

.clear_flag:
    LDA #$00
    STA.l !AP_EXECUTE_FLAG

.done:
    PLX
    PLP
    RTL

AP_BitMaskTable:
    db $01, $02, $04, $08, $10, $20, $40, $80

AP_WeaponAddressTable:
    dw $0B85 ; $01 Freeze Cracker
    dw $0B91 ; $02 Danger Wrap
    dw $0B87 ; $03 Thunder Bolt
    dw $0B89 ; $04 Junk Shield
    dw $0B8D ; $05 Slash Claw
    dw $0B93 ; $06 Wild Coil
    dw $0B8F ; $07 Noise Crush
    dw $0B8B ; $08 Scorch Wheel
    dw $0B9B ; $09 Rush Coil
    dw $0B97 ; $0A Rush Search
    dw $0B99 ; $0B Rush Jet

AP_EnsureVanillaWilyAvailable:
    ; $0B7C must be nonzero for the vanilla stage-select Wily box setup.
    ; AP_SELECTED_WILY_STAGE remains the AP-owned selected Wily stage.
    LDA.l $7E0B7C
    BNE .done

    LDA #$01
    STA.l $7E0B7C

.done:
    RTS

; ============================================
; Boss defeated/check flag tables and hooks
; ============================================

AP_BossBitMaskTable:
    db $00 ; index 0 unused / unknown
    db $01 ; index 1 = Freeze Man
    db $02 ; index 2 = Cloud Man
    db $04 ; index 3 = Junk Man
    db $08 ; index 4 = Turbo Man
    db $10 ; index 5 = Slash Man
    db $20 ; index 6 = Shade Man
    db $40 ; index 7 = Burst Man
    db $80 ; index 8 = Spring Man

AP_StageSelectBitMaskTable:
    db $00 ; index 0 unused
    db $01 ; X=$02
    db $02 ; X=$04
    db $04 ; X=$06
    db $08 ; X=$08
    db $10 ; X=$0A
    db $20 ; X=$0C
    db $40 ; X=$0E
    db $80 ; X=$10

AP_LoadBossDefeatedState:
    PHP
    SEP #$30
    PHX

    ; X is stage_id * 2 here.
    TXA
    LSR
    TAX

    LDA.l AP_BossBitMaskTable,x
    AND.l !AP_BOSS_FLAGS
    BEQ .not_defeated

.defeated:
    PLX
    PLP
    SEC
    LDA #$80
    RTL

.not_defeated:
    PLX
    PLP
    CLC
    LDA #$00
    RTL

AP_ProtoCloudMeetingGate:
    PHP
    SEP #$20

    ; If AP already recorded this Proto Man meeting check, skip it.
    LDA.l !AP_PROTO_CHECKS
    AND #$01
    BNE .Skip

    ; Otherwise record the AP check and continue to vanilla meeting/event path.
    LDA.l !AP_PROTO_CHECKS
    ORA #$01
    STA.l !AP_PROTO_CHECKS

    PLP
    JML $C2C4ED

.Skip:
    PLP
    JML $C2C4BF

AP_ProtoTurboMeetingGate:
    PHP
    SEP #$20

    ; If AP already recorded this Proto Man meeting check, skip it.
    LDA.l !AP_PROTO_CHECKS
    AND #$02
    BNE .skip

    ; Otherwise record the AP check and continue to vanilla meeting/event path.
    LDA.l !AP_PROTO_CHECKS
    ORA #$02
    STA.l !AP_PROTO_CHECKS

    PLP
    JML $C2C4ED

.skip:
    PLP
    JML $C2C4BF

AP_ProtoShieldEncounterGate:
    PHP
    SEP #$20

    ; If Proto Shield location is already checked, skip the encounter.
    LDA.l !AP_PROTO_CHECKS
    AND #$04
    BNE .skip

    ; Require both AP Proto clue items.
    ; bit $01 = Cloud clue item received
    ; bit $02 = Turbo clue item received
    LDA.l !AP_PROTO_ITEMS
    AND #$03
    CMP #$03
    BEQ .allow

.skip:
    PLP
    JML $C2C4E5

.allow:
    PLP
    JML $C2C4ED

AP_ProtoShieldRewardCheck:
    PHP
    SEP #$20

    ; Mark Proto Shield location checked.
    ; bit $04 of AP_PROTO_CHECKS.
    LDA.l !AP_PROTO_CHECKS
    ORA #$04
    STA.l !AP_PROTO_CHECKS

    PLP

    ; Skip vanilla Proto Shield grant and continue post-fight flow.
    JML $C37233

AP_StageExitAPOnlyBossGate:
    PHP
    SEP #$30
    PHX

    ; X is stage_id * 2 here.
    ; Record the boss as defeated for AP.
    TXA
    LSR
    TAX

    LDA.l AP_BossBitMaskTable,x
    ORA.l !AP_BOSS_FLAGS
    STA.l !AP_BOSS_FLAGS

    PLX
    PLP

    ; Skip vanilla weapon-get / boss weapon grant.
    JML $C00DDC

AP_WilyUnlockGate:
    ; Wily access is item-gated by AP Wily Access Codes.
    ; Do not unlock vanilla Wily just because all 8 Robot Masters are defeated.
    PHP
    SEP #$20

    LDA.l !AP_WILY_ACCESS
    AND #$07
    BNE .has_wily_access

.no_wily_access:
    PLP
    JML $C00E08

.has_wily_access:
    PLP
    JML $C00DEC

AP_WilyCapsuleDefeatedHook:
    PHP
    SEP #$20

    ; Preserve replaced vanilla behavior: INC $0BCA
    LDA.l $7E0BCA
    INC
    STA.l $7E0BCA

    ; Mark AP goal complete.
    LDA.l !AP_GOAL_FLAGS
    ORA #$01
    STA.l !AP_GOAL_FLAGS

    ; Preserve replaced vanilla behavior: LDA #$08
    LDA #$08

    PLP
    RTL

AP_RushSearchSpawnCheck:
    PHP
    SEP #$20

    ; If AP already checked Rush Search Location, despawn/skip it.
    LDA.l !AP_RUSH_FLAGS
    AND #$01
    BNE .already_checked

    ; Otherwise allow the object to spawn, even if $0B97 says Rush Search is owned.
    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF

AP_RushSearchPickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_RUSH_FLAGS
    ORA #$01
    STA.l !AP_RUSH_FLAGS

    PLP
    JML $D8D1E7

AP_ShopRushSearchCheck:
    PHP
    SEP #$20

    LDA.l !AP_RUSH_FLAGS
    AND #$01
    BNE .already_checked

    PLP
    JML $D8D9CC

.already_checked:
    PLP
    JML $D8D99E

AP_ShopRushSearchPurchase:
    PHP
    SEP #$20

    LDA.l !AP_RUSH_FLAGS
    ORA #$01
    STA.l !AP_RUSH_FLAGS

    PLP
    RTS

AP_RushJetSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_RUSH_FLAGS
    AND #$02
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF

AP_RushJetPickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_RUSH_FLAGS
    ORA #$02
    STA.l !AP_RUSH_FLAGS

    PLP
    JML $D8D1E7

AP_ShopRushJetCheck:
    PHP
    SEP #$20

    LDA.l !AP_RUSH_FLAGS
    AND #$02
    BNE .already_checked

    PLP
    JML $D8D9C5

.already_checked:
    PLP
    JML $D8D99E        ; vanilla unavailable path

AP_ShopRushJetPurchase:
    PHP
    SEP #$20

    LDA.l !AP_RUSH_FLAGS
    ORA #$02
    STA.l !AP_RUSH_FLAGS

    PLP
    RTS

AP_FreezeManPresenceGate:
    PHP
    SEP #$30
    PHX

    LDA.l $7E0B73
    CMP #$09
    BCS .continue

    TAX

    LDA.l AP_BossBitMaskTable,x
    AND.l !AP_BOSS_FLAGS
    BNE .skip_object

.continue:
    PLX
    PLP
    JML $C286FC

.skip_object:
    PLX
    PLP
    JML $C286FB

AP_RushRPlatePickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$01
    STA.l !AP_ITEM_FLAGS

    PLP
    JSR $D1D0
    JML $D8D1E7

AP_RushUPlatePickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$02
    STA.l !AP_ITEM_FLAGS

    PLP

    ; Preserve vanilla plate pickup side effect.
    JSR $D1D0

    ; Skip vanilla plate grant and continue normal pickup cleanup.
    JML $D8D1E7

AP_RushSPlatePickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$04
    STA.l !AP_ITEM_FLAGS

    PLP

    ; Preserve vanilla plate pickup side effect.
    JSR $D1D0

    ; Skip vanilla plate grant and continue normal pickup cleanup.
    JML $D8D1E7

AP_RushHPlatePickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$08
    STA.l !AP_ITEM_FLAGS

    PLP

    ; Preserve vanilla plate pickup side effect.
    JSR $D1D0

    ; Skip vanilla plate grant and continue normal pickup cleanup.
    JML $D8D1E7

AP_RushRPlateSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$01
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF


AP_RushUPlateSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$02
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF


AP_RushSPlateSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$04
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF


AP_RushHPlateSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$08
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF

AP_ExitUnitPickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$20
    STA.l !AP_ITEM_FLAGS

    PLP
    JML $D8D1E7

AP_ShopExitUnitCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$20
    BNE .already_checked

    PLP
    JML $D8D99C

.already_checked:
    PLP
    JML $D8D99E

AP_ShopExitUnitPurchase:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$20
    STA.l !AP_ITEM_FLAGS

    PLP
    RTS

AP_EnergyBalancerPickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$80
    STA.l !AP_ITEM_FLAGS

    PLP
    JML $D8D1E7

AP_ShopEnergyBalancerCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$80
    BNE .already_checked

    PLP
    JML $D8D9AF

.already_checked:
    PLP
    JML $D8D99E

AP_ShopEnergyBalancerPurchase:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$80
    STA.l !AP_ITEM_FLAGS

    PLP
    RTS

AP_HyperBoltPickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$10
    STA.l !AP_ITEM_FLAGS

    PLP
    JML $D8D1E7

AP_HyperRocketBusterPickupCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$40
    STA.l !AP_ITEM_FLAGS

    PLP
    JML $D8D1E7

AP_ShopHyperRocketBusterCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$40
    BNE .already_checked

    PLP
    JML $D8D9BE

.already_checked:
    PLP
    JML $D8D99E

AP_ShopHyperRocketBusterSuperAdapterGate:
    JML $D8D75F

AP_ShopHyperRocketBusterPurchase:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    ORA #$40
    STA.l !AP_ITEM_FLAGS

    PLP
    RTS

AP_ExitUnitSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$20
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF

AP_ExitUnitRushSearchGate:
    PHP
    SEP #$30

    LDX #$1B

    ; If AP already checked Exit Unit Location, skip it.
    LDA.l !AP_ITEM_FLAGS
    AND #$20
    BNE .already_checked

    ; Otherwise allow the search result.
    PLP
    JML $C14D88

.already_checked:
    PLP
    JML $C14D96

AP_ExitUnitMedalCheck:
    PHP
    SEP #$30
    PHX

    ; X is the vanilla offset into $0B83 table.
    ; Convert $02,$04,...,$10 into boss index 1..8.
    TXA
    LSR
    TAX

    LDA.l AP_BossBitMaskTable,x
    AND.l !AP_BOSS_FLAGS
    BEQ .no_medal

.has_medal:
    PLX
    PLP
    JML $C047F0

.no_medal:
    PLX
    PLP
    JML $C04807


AP_EnergyBalancerSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$80
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF

AP_EnergyBalancerRushSearchGate:
    PHP
    SEP #$30

    LDX #$1D

    ; If AP already checked Energy Balancer Location, skip it.
    LDA.l !AP_ITEM_FLAGS
    AND #$80
    BNE .already_checked

    ; Otherwise allow the search result.
    PLP
    JML $C14D88

.already_checked:
    PLP
    JML $C14DB3


AP_HyperBoltSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$10
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF


AP_HyperRocketBusterSpawnCheck:
    PHP
    SEP #$20

    LDA.l !AP_ITEM_FLAGS
    AND #$40
    BNE .already_checked

    PLP
    RTS

.already_checked:
    PLP
    JML $D8D1DF

AP_HyperRocketBusterRushSearchGate:
    PHP
    SEP #$30

    ; Always use the Hyper Rocket Buster Rush Search result,
    ; even if Super Adapter is not owned.
    LDX #$1C

    ; If AP already checked Hyper Rocket Buster Location, skip it.
    LDA.l !AP_ITEM_FLAGS
    AND #$40
    BNE .already_checked

    ; Otherwise allow the search result.
    PLP
    JML $C14D88

.already_checked:
    PLP
    JML $C14DA8

AP_MegaItemRushSearchCheck:
    PHP
    SEP #$30

    LDA #$01

.loop:
    DEX
    DEX
    BMI .check
    ASL
    BRA .loop

.check:
    STA.l !AP_TEMP

    LDA.l !AP_MEGA_FLAGS
    AND.l !AP_TEMP
    BNE .already_checked

    LDA.l !AP_MEGA_FLAGS
    ORA.l !AP_TEMP
    STA.l !AP_MEGA_FLAGS

    LDX $0000

    PLP
    JML $C14D88

.already_checked:
    PLP
    JML $C14D80

AP_BeatEncounterGate:
    PHP
    SEP #$20

    LDA.l !AP_MISC_FLAGS
    AND #$01
    BNE .already_checked

    PLP
    JML $C35121

.already_checked:
    PLP
    JSL $C108EF
    JML $C35120

AP_BeatRewardCheck:
    PHP
    SEP #$20

    ; Mark Beat Location checked.
    LDA.l !AP_MISC_FLAGS
    ORA #$01
    STA.l !AP_MISC_FLAGS

    PLP

    ; Skip vanilla Beat inventory grant and continue the original sequence.
    JML $D8CE92

AP_IntroStageClearCheck:
    PHP
    SEP #$20

    ; Preserve vanilla behavior: mark Intro Stage cleared.
    STZ $0B79

    ; Mark Rush Coil / Intro Stage clear location checked.
    LDA.l !AP_RUSH_FLAGS
    ORA #$04
    STA.l !AP_RUSH_FLAGS

    ; Preserve vanilla behavior.
    LDA #$04
    STA $DF

    PLP

    ; Preserve vanilla transition.
    JML $C06739

AP_RobotMuseumRouteGate:
    PHP
    SEP #$30
    PHX

    ; If Mash was already checked, use normal route.
    LDA.l !AP_MISC_FLAGS
    AND #$02        ; $02 = Mash checked
    BNE .normal_route

    ; Count AP defeated Robot Masters.
    LDA.l !AP_BOSS_FLAGS
    STA.l !AP_TEMP

    LDX #$00

.count_loop:
    LDA.l !AP_TEMP
    BEQ .not_enough

    LSR
    STA.l !AP_TEMP

    BCC .next_bit

    INX
    CPX #$04
    BCS .go_robot_museum

.next_bit:
    BRA .count_loop

.go_robot_museum:
    PLX
    PLP
    JML $C00C72

.not_enough:
.normal_route:
    PLX
    PLP
    JML $C00C7E

AP_RobotMuseumClearCheck:
    PHP
    SEP #$20

    ; Preserve vanilla behavior.
    INC $0B7A

    ; Mark Mash / Robot Museum location checked.
    LDA.l !AP_MISC_FLAGS
    ORA #$02
    STA.l !AP_MISC_FLAGS

    PLP

    ; Preserve vanilla branch.
    JML $C00E08

AP_WilyStageClearCheck:
    PHP
    SEP #$20

    ; Use AP-selected Wily stage, not vanilla $0B7C.
    ; Wily 1/2/3 can now be cleared out of vanilla order.
    LDA.l !AP_SELECTED_WILY_STAGE

    CMP #$01
    BEQ .clear_wily_1

    CMP #$02
    BEQ .clear_wily_2

    CMP #$03
    BEQ .clear_wily_3

    CMP #$04
    BEQ .clear_wily_4

    ; Unknown/no selected Wily stage. Fall back to vanilla behavior.
    PLP
    LDA.l $7E0B7C
    INC
    STA.l $7E0B7C
    JML $C00DFF

.clear_wily_1:
    LDA.l !AP_WILY_FLAGS
    ORA #$01
    STA.l !AP_WILY_FLAGS
    BRA .return_to_stage_select

.clear_wily_2:
    LDA.l !AP_WILY_FLAGS
    ORA #$02
    STA.l !AP_WILY_FLAGS
    BRA .return_to_stage_select

.clear_wily_3:
    LDA.l !AP_WILY_FLAGS
    ORA #$04
    STA.l !AP_WILY_FLAGS
    BRA .return_to_stage_select

.clear_wily_4:
    ; Wily 4 / Capsule keeps vanilla final-stage behavior.
    ; AP goal is handled by AP_WilyCapsuleDefeatedHook.
    LDA #$00
    STA.l !AP_SELECTED_WILY_STAGE

    PLP

    LDA.l $7E0B7C
    INC
    STA.l $7E0B7C
    JML $C00DFF

.return_to_stage_select:
    ; The selected Wily stage is now consumed.
    LDA #$00
    STA.l !AP_SELECTED_WILY_STAGE

    PLP

    ; Do not continue vanilla Wily progression for AP Wily 1/2/3.
    JML $C00E08

AP_GetSelectedWilyStageId:
    PHP
    SEP #$20

    ; Keep the player's L/R selection if it is still available.
    LDA.l !AP_SELECTED_WILY_STAGE
    BEQ .choose_first

    JSR AP_IsSelectedWilyStageAvailable
    BCS .use_selected

.choose_first:
    JSR AP_SelectFirstAvailableWilyStage

    LDA.l !AP_SELECTED_WILY_STAGE
    BEQ .no_available_stage

.use_selected:
    LDA.l !AP_SELECTED_WILY_STAGE
    CLC
    ADC #$09

    PLP
    RTL

.no_available_stage:
    ; The confirm hook should prevent this routine from being used when
    ; no AP Wily stage is available. Return 0 as a defensive fallback.
    LDA #$00

    PLP
    RTL

AP_HasAnyAvailableWilyStage:
    PHP
    SEP #$20

    ; Keep the player's L/R selection if it is still available.
    LDA.l !AP_SELECTED_WILY_STAGE
    BEQ .choose_first

    JSR AP_IsSelectedWilyStageAvailable
    BCS .available

.choose_first:
    JSR AP_SelectFirstAvailableWilyStage

    LDA.l !AP_SELECTED_WILY_STAGE
    BEQ .none

.available:
    PLP
    SEC
    RTL

.none:
    PLP
    CLC
    RTL

AP_SelectFirstAvailableWilyStage:
    ; Wily 1 available if access code owned and stage not cleared.
    LDA.l !AP_WILY_ACCESS
    AND #$01
    BEQ .check_2

    LDA.l !AP_WILY_FLAGS
    AND #$01
    BNE .check_2

    LDA #$01
    STA.l !AP_SELECTED_WILY_STAGE
    RTS

.check_2:
    ; Wily 2 available if access code owned and stage not cleared.
    LDA.l !AP_WILY_ACCESS
    AND #$02
    BEQ .check_3

    LDA.l !AP_WILY_FLAGS
    AND #$02
    BNE .check_3

    LDA #$02
    STA.l !AP_SELECTED_WILY_STAGE
    RTS

.check_3:
    ; Wily 3 available if access code owned and stage not cleared.
    LDA.l !AP_WILY_ACCESS
    AND #$04
    BEQ .check_4

    LDA.l !AP_WILY_FLAGS
    AND #$04
    BNE .check_4

    LDA #$03
    STA.l !AP_SELECTED_WILY_STAGE
    RTS

.check_4:
    ; Wily 4 available after Wily 1-3 are cleared.
    LDA.l !AP_WILY_FLAGS
    AND #$07
    CMP #$07
    BNE .none

    LDA #$04
    STA.l !AP_SELECTED_WILY_STAGE
    RTS

.none:
    LDA #$00
    STA.l !AP_SELECTED_WILY_STAGE
    RTS

AP_SelectNextAvailableWilyStage:
    LDA.l !AP_SELECTED_WILY_STAGE
    INC
    CMP #$05
    BCC .store_candidate

    LDA #$01

.store_candidate:
    STA.l !AP_SELECTED_WILY_STAGE

    JSR AP_IsSelectedWilyStageAvailable
    BCS .done

    LDA.l !AP_SELECTED_WILY_STAGE
    INC
    CMP #$05
    BCC .store_candidate_2

    LDA #$01

.store_candidate_2:
    STA.l !AP_SELECTED_WILY_STAGE

    JSR AP_IsSelectedWilyStageAvailable
    BCS .done

    LDA.l !AP_SELECTED_WILY_STAGE
    INC
    CMP #$05
    BCC .store_candidate_3

    LDA #$01

.store_candidate_3:
    STA.l !AP_SELECTED_WILY_STAGE

    JSR AP_IsSelectedWilyStageAvailable
    BCS .done

    LDA.l !AP_SELECTED_WILY_STAGE
    INC
    CMP #$05
    BCC .store_candidate_4

    LDA #$01

.store_candidate_4:
    STA.l !AP_SELECTED_WILY_STAGE

    JSR AP_IsSelectedWilyStageAvailable
    BCS .done

    ; No available Wily stage.
    LDA #$00
    STA.l !AP_SELECTED_WILY_STAGE

.done:
    RTL

AP_SelectPreviousAvailableWilyStage:
    LDA.l !AP_SELECTED_WILY_STAGE
    DEC
    BNE .store_candidate

    LDA #$04

.store_candidate:
    STA.l !AP_SELECTED_WILY_STAGE

    JSR AP_IsSelectedWilyStageAvailable
    BCS .done

    LDA.l !AP_SELECTED_WILY_STAGE
    DEC
    BNE .store_candidate_2

    LDA #$04

.store_candidate_2:
    STA.l !AP_SELECTED_WILY_STAGE

    JSR AP_IsSelectedWilyStageAvailable
    BCS .done

    LDA.l !AP_SELECTED_WILY_STAGE
    DEC
    BNE .store_candidate_3

    LDA #$04

.store_candidate_3:
    STA.l !AP_SELECTED_WILY_STAGE

    JSR AP_IsSelectedWilyStageAvailable
    BCS .done

    LDA.l !AP_SELECTED_WILY_STAGE
    DEC
    BNE .store_candidate_4

    LDA #$04

.store_candidate_4:
    STA.l !AP_SELECTED_WILY_STAGE

    JSR AP_IsSelectedWilyStageAvailable
    BCS .done

    ; No available Wily stage.
    LDA #$00
    STA.l !AP_SELECTED_WILY_STAGE

.done:
    RTL

AP_IsSelectedWilyStageAvailable:
    LDA.l !AP_SELECTED_WILY_STAGE

    CMP #$01
    BEQ .stage_1

    CMP #$02
    BEQ .stage_2

    CMP #$03
    BEQ .stage_3

    CMP #$04
    BEQ .stage_4

.unavailable:
    CLC
    RTS

.stage_1:
    LDA.l !AP_WILY_ACCESS
    AND #$01
    BEQ .unavailable

    LDA.l !AP_WILY_FLAGS
    AND #$01
    BNE .unavailable

    SEC
    RTS

.stage_2:
    LDA.l !AP_WILY_ACCESS
    AND #$02
    BEQ .unavailable

    LDA.l !AP_WILY_FLAGS
    AND #$02
    BNE .unavailable

    SEC
    RTS

.stage_3:
    LDA.l !AP_WILY_ACCESS
    AND #$04
    BEQ .unavailable

    LDA.l !AP_WILY_FLAGS
    AND #$04
    BNE .unavailable

    SEC
    RTS

.stage_4:
    LDA.l !AP_WILY_FLAGS
    AND #$07
    CMP #$07
    BNE .unavailable

    SEC
    RTS

AP_DrawSelectedWilyStageNumber:
    PHP
    SEP #$30
    PHX

    ; Ensure a selected Wily stage exists if any Wily stage is available.
    JSL AP_HasAnyAvailableWilyStage
    BCC .hide

    ; X = selected Wily stage: 1-4
    LDA.l !AP_SELECTED_WILY_STAGE
    TAX

    ; slot 124 = $0700 + 4 * 124 = $08F0
    ; high OAM byte = $0900 + floor(124 / 4) = $091F

    LDA.l AP_WilyStageNumberTileTable,x
    STA.l $7E08F2

    LDA #$90
    STA.l $7E08F0 ; X

    LDA #$58
    STA.l $7E08F1 ; Y

    LDA #$3F
    STA.l $7E08F3 ; attrs

    ; Slot 124 uses bits 0-1 of $091F.
    ; Clear only slot 124's high-OAM bits.
    LDA.l $7E091F
    AND #$FC
    STA.l $7E091F

    PLX
    PLP
    RTL

.hide:
    LDA #$E0
    STA.l $7E08F1

    PLX
    PLP
    RTL

AP_WilyStageNumberTileTable:
    db $00
    db $25
    db $26
    db $27
    db $28

; ============================================
; AP ROM auth token
;
; Written by rom.py after the base bsdiff is applied.
; Client reads this from ROM and uses it as ctx.rom.
;
; File offset: $18FEC0
; CPU addr:    $D8FEC0
; Size:        32 bytes
; ============================================

assert pc() <= $D8FEC0

org $D8FEC0
AP_ROM_AUTH_TOKEN:
    db "MM7AP"
    fillbyte $00
    fill 27

assert pc() <= $D8FF00